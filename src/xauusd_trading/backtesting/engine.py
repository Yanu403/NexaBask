from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from xauusd_trading.backtesting.trailing import simulate_long_with_optional_trailing, simulate_short_with_optional_trailing
from xauusd_trading.models.trading import ExecutedTrade, TradeSignal
from xauusd_trading.risk.manager import RiskConfig, RiskManager
from xauusd_trading.strategies.base import Strategy


@dataclass(slots=True)
class BacktestConfig:
    initial_balance: float = 10_000.0
    slippage_pct: float = 0.04
    risk: RiskConfig = field(default_factory=RiskConfig)
    max_open_positions: int = 999


class BacktestEngine:
    def __init__(self, config: BacktestConfig | None = None) -> None:
        self.config = config or BacktestConfig()
        self.last_risk_summary: dict[str, float | str | None] = {}

    def run(self, df: pd.DataFrame, strategy: Strategy) -> list[ExecutedTrade]:
        feature_df = strategy.prepare_features(df)
        risk_manager = RiskManager(initial_balance=self.config.initial_balance, config=self.config.risk)
        trades: list[ExecutedTrade] = []
        last_exit_index = -1

        # ── Optimization: pre-compute trade-window indices ──────────────
        # Instead of iterating ALL ~24K bars (only ~8K are trade-window),
        # detect which bars could possibly produce a signal.
        tw_col = None
        for col in ('is_trade_window', 'is_london_window'):
            if col in feature_df.columns:
                tw_col = col
                break

        if tw_col is not None:
            # Fast positional index array using numpy
            import numpy as np
            tw_mask = feature_df[tw_col].values == 1
            candidate_pos = np.where(tw_mask)[0].tolist()
        else:
            candidate_pos = list(range(len(feature_df) - 1))

        for index in candidate_pos:
            if not risk_manager.can_open_trade():
                break

            if self.config.max_open_positions <= 1 and index <= last_exit_index:
                continue

            signal = strategy.generate_signal(feature_df, index)
            if signal is None:
                continue

            # Need a next bar to enter the trade at next-bar-open
            if signal.index + 1 >= len(feature_df):
                continue

            try:
                trade = self._simulate_trade(feature_df, signal, risk_manager)
            except ValueError:
                # Signal geometry invalid (e.g. SL/TP violates side constraints) – skip
                continue
            trades.append(trade)
            risk_manager.register_trade(trade.pnl_currency)
            last_exit_index = max(last_exit_index, trade.exit_index)

        self.last_risk_summary = risk_manager.summary()
        return trades

    def _simulate_trade(self, df: pd.DataFrame, signal: TradeSignal, risk_manager: RiskManager) -> ExecutedTrade:
        # ── 1. Compute actual entry: next-bar open + spread ─────────────
        next_bar_idx = signal.index + 1
        if next_bar_idx >= len(df):
            raise ValueError("Signal at last bar, no next bar for entry")
        next_bar = df.iloc[next_bar_idx]

        pip_size = float(signal.metadata.get("pip_size", 0.0001))
        spread_points_per_pip = float(signal.metadata.get("spread_points_per_pip", 10.0))
        if "spread" in df.columns:
            spread_price = float(next_bar["spread"]) * pip_size / spread_points_per_pip
        else:
            spread_price = 0.0

        if signal.side == "LONG":
            actual_entry = float(next_bar["open"]) + spread_price
        else:
            actual_entry = float(next_bar["open"]) - spread_price

        # ── 2. Adjust SL/TP relative to actual entry ─────────────────────
        # Keep the same risk:reward distances as the strategy intended.
        signal_risk_dist = abs(signal.entry_price - signal.stop_loss)
        signal_tp_dist = abs(signal.take_profit - signal.entry_price)
        if signal.side == "LONG":
            actual_sl = actual_entry - signal_risk_dist
            actual_tp = actual_entry + signal_tp_dist
        else:
            actual_sl = actual_entry + signal_risk_dist
            actual_tp = actual_entry - signal_tp_dist

        # Validate geometry
        if actual_entry <= 0:
            raise ValueError(f"entry_price must be > 0, got {actual_entry}")
        if signal.side == "LONG" and not (actual_sl < actual_entry < actual_tp):
            raise ValueError(f"LONG requires SL < entry < TP, got SL={actual_sl}, entry={actual_entry}, TP={actual_tp}")
        if signal.side == "SHORT" and not (actual_tp < actual_entry < actual_sl):
            raise ValueError(f"SHORT requires TP < entry < SL, got TP={actual_tp}, entry={actual_entry}, SL={actual_sl}")

        # ── 3. Build adjusted signal for trailing simulation ─────────────
        adjusted_signal = TradeSignal(
            index=next_bar_idx,
            timestamp=df.index[next_bar_idx],
            side=signal.side,
            entry_price=actual_entry,
            stop_loss=actual_sl,
            take_profit=actual_tp,
            max_hold_bars=max(signal.max_hold_bars - 1, 1),
            metadata=signal.metadata,
        )

        # ── 4. Run trailing simulation with adjusted signal ──────────────
        exit_index = min(adjusted_signal.index + adjusted_signal.max_hold_bars, len(df) - 1)
        trailing_atr_multiple = signal.metadata.get("trail_atr_multiple")
        partial_tp_rr = signal.metadata.get("partial_tp_rr")
        partial_close_fraction = float(signal.metadata.get("partial_close_fraction", 0.5))
        move_stop_to_breakeven = bool(signal.metadata.get("move_stop_to_breakeven_on_partial", True))

        if signal.side == "LONG":
            exit_price, exit_reason, exit_index, extra_metadata = simulate_long_with_optional_trailing(
                df,
                adjusted_signal,
                trailing_atr_multiple=trailing_atr_multiple if trailing_atr_multiple is not None else None,
                partial_tp_rr=partial_tp_rr if partial_tp_rr is not None else None,
                partial_close_fraction=partial_close_fraction,
                move_stop_to_breakeven_on_partial=move_stop_to_breakeven,
                default_exit_index=exit_index,
            )
            raw_pnl_pct = (exit_price - actual_entry) / actual_entry * 100
        else:
            exit_price, exit_reason, exit_index, extra_metadata = simulate_short_with_optional_trailing(
                df,
                adjusted_signal,
                trailing_atr_multiple=trailing_atr_multiple if trailing_atr_multiple is not None else None,
                partial_tp_rr=partial_tp_rr if partial_tp_rr is not None else None,
                partial_close_fraction=partial_close_fraction,
                move_stop_to_breakeven_on_partial=move_stop_to_breakeven,
                default_exit_index=exit_index,
            )
            raw_pnl_pct = (actual_entry - exit_price) / actual_entry * 100

        # ── 5. Slippage on pct ───────────────────────────────────────────
        if raw_pnl_pct > 0:
            pnl_pct = max(raw_pnl_pct - self.config.slippage_pct, 0.0)
        elif raw_pnl_pct < 0:
            pnl_pct = min(raw_pnl_pct + self.config.slippage_pct, 0.0)
        else:
            pnl_pct = 0.0

        # ── 6. Position sizing based on ACTUAL risk distance ─────────────
        risk_amount, position_size = risk_manager.size_position(
            entry_price=actual_entry, stop_loss=actual_sl,
            pip_size=pip_size,
        )
        if position_size <= 0:
            raise ValueError("Position size zero — stop too tight")

        if signal.side == "LONG":
            pnl_currency = position_size * (exit_price - actual_entry)
        else:
            pnl_currency = position_size * (actual_entry - exit_price)

        # Apply execution slippage to currency PnL
        if pnl_currency > 0:
            pnl_currency *= (1 - self.config.slippage_pct / 100)
        elif pnl_currency < 0:
            pnl_currency *= (1 + self.config.slippage_pct / 100)

        equity_before = risk_manager.balance
        equity_after = equity_before + pnl_currency

        metadata = {**signal.metadata, **extra_metadata, "actual_entry_price": actual_entry}

        return ExecutedTrade(
            entry_index=next_bar_idx,
            exit_index=exit_index,
            entry_time=df.index[next_bar_idx],
            exit_time=df.index[exit_index],
            side=signal.side,
            entry_price=actual_entry,
            exit_price=exit_price,
            stop_loss=actual_sl,
            take_profit=actual_tp,
            exit_reason=exit_reason,
            pnl_pct=pnl_pct,
            pnl_currency=pnl_currency,
            position_size=position_size,
            risk_amount=risk_amount,
            equity_before=equity_before,
            equity_after=equity_after,
            metadata=metadata,
        )
