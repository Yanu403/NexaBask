from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pandas as pd

from xauusd_trading.data.loader import load_ohlcv_csv
from xauusd_trading.models.paper import PaperPosition, PaperState
from xauusd_trading.models.trading import TradeSignal
from xauusd_trading.risk.manager import RiskConfig, RiskManager


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_paper_state(path: str | Path, *, data_path: str, initial_balance: float = 10_000.0) -> PaperState:
    state_path = Path(path)
    if not state_path.exists():
        return PaperState(
            generated_at=_utc_now(),
            data_path=data_path,
            balance=initial_balance,
            peak_balance=initial_balance,
            closed_trades=0,
            open_positions=[],
        )

    payload = json.loads(state_path.read_text())
    return PaperState(
        generated_at=payload.get('generated_at', _utc_now()),
        data_path=payload.get('data_path', data_path),
        balance=payload.get('balance', initial_balance),
        peak_balance=payload.get('peak_balance', initial_balance),
        closed_trades=payload.get('closed_trades', 0),
        open_positions=[PaperPosition(**position) for position in payload.get('open_positions', [])],
        journal_path=payload.get('journal_path'),
    )


def save_paper_state(state: PaperState, path: str | Path) -> Path:
    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state.generated_at = _utc_now()
    state_path.write_text(json.dumps(state.to_dict(), indent=2))
    return state_path


class PaperTrader:
    def __init__(self, *, state: PaperState, risk_config: RiskConfig | None = None) -> None:
        self.state = state
        self.risk_manager = RiskManager(initial_balance=state.balance, config=risk_config or RiskConfig())
        self.risk_manager.balance = state.balance
        self.risk_manager.peak_balance = max(state.peak_balance, state.balance)
        self.events: list[dict] = []
        self.last_step_events: list[dict] = []

    def step(self, *, df: pd.DataFrame, signals: list[TradeSignal], journal_path: str | Path) -> PaperState:
        last_index = len(df) - 1
        self._update_open_positions(df, last_index)

        if not self.state.open_positions and signals and self.risk_manager.can_open_trade():
            signal = sorted(signals, key=lambda item: (item.metadata.get('strategy_priority', 999), item.side))[0]
            self._open_position(signal, journal_path)

        self.state.balance = self.risk_manager.balance
        self.state.peak_balance = self.risk_manager.peak_balance
        self.state.journal_path = str(journal_path)
        self._append_journal(journal_path)
        self.last_step_events = list(self.events)
        self.events = []
        return self.state

    def _open_position(self, signal: TradeSignal, journal_path: str | Path) -> None:
        risk_per_trade_override = signal.metadata.get('risk_per_trade')
        if isinstance(risk_per_trade_override, (int, float)) and float(risk_per_trade_override) > 0:
            stop_distance = abs(signal.entry_price - signal.stop_loss)
            risk_amount = self.risk_manager.balance * float(risk_per_trade_override)
            position_size = risk_amount / stop_distance if stop_distance > 0 else 0.0
        else:
            risk_amount, position_size = self.risk_manager.size_position(entry_price=signal.entry_price, stop_loss=signal.stop_loss)
        position = PaperPosition(
            position_id=uuid4().hex[:12],
            strategy=str(signal.metadata.get('strategy', 'unknown')),
            side=signal.side,
            entry_index=signal.index,
            last_processed_index=signal.index,
            entry_time=signal.timestamp.isoformat(),
            entry_price=signal.entry_price,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            max_hold_bars=signal.max_hold_bars,
            position_size=position_size,
            risk_amount=risk_amount,
            trail_atr_multiple=signal.metadata.get('trail_atr_multiple'),
            partial_tp_rr=signal.metadata.get('partial_tp_rr'),
            partial_close_fraction=float(signal.metadata.get('partial_close_fraction', 0.5)),
            move_stop_to_breakeven_on_partial=bool(signal.metadata.get('move_stop_to_breakeven_on_partial', True)),
            metadata=dict(signal.metadata),
        )
        self.state.open_positions.append(position)
        self.events.append({'type': 'OPEN', 'position': position.to_dict(), 'journal_path': str(journal_path)})

    def _update_open_positions(self, df: pd.DataFrame, last_index: int) -> None:
        remaining: list[PaperPosition] = []
        for position in self.state.open_positions:
            closed = self._advance_position(position, df, last_index)
            if closed is None:
                remaining.append(position)
            else:
                self.state.closed_trades += 1
        self.state.open_positions = remaining

    def _advance_position(self, position: PaperPosition, df: pd.DataFrame, last_index: int) -> dict | None:
        stop_distance = abs(position.entry_price - position.stop_loss)
        partial_tp_price = None
        if position.partial_tp_rr is not None:
            if position.side == 'LONG':
                partial_tp_price = position.entry_price + stop_distance * position.partial_tp_rr
            else:
                partial_tp_price = position.entry_price - stop_distance * position.partial_tp_rr

        timeout_index = min(position.entry_index + position.max_hold_bars, last_index)
        for index in range(position.last_processed_index + 1, last_index + 1):
            row = df.iloc[index]
            high = float(row['high'])
            low = float(row['low'])
            close = float(row['close'])
            atr = float(row.get('atr14', 0.0)) if 'atr14' in row.index else 0.0

            if position.side == 'LONG':
                if not position.partial_taken and partial_tp_price is not None and high >= partial_tp_price:
                    position.partial_taken = True
                    position.partial_exit_price = partial_tp_price
                    position.partial_exit_index = index
                    if position.move_stop_to_breakeven_on_partial:
                        position.stop_loss = max(position.stop_loss, position.entry_price)

                take_profit_half = position.entry_price + (position.take_profit - position.entry_price) * 0.5
                if position.trail_atr_multiple is not None and high >= take_profit_half and atr > 0:
                    position.stop_loss = max(position.stop_loss, close - atr * position.trail_atr_multiple)

                if high >= position.take_profit:
                    return self._close_position(position, index, position.take_profit, 'TP_HIT', df)
                if low <= position.stop_loss:
                    reason = 'TRAIL' if position.partial_taken and position.stop_loss >= position.entry_price else 'SL_HIT'
                    return self._close_position(position, index, position.stop_loss, reason, df)
            else:
                if not position.partial_taken and partial_tp_price is not None and low <= partial_tp_price:
                    position.partial_taken = True
                    position.partial_exit_price = partial_tp_price
                    position.partial_exit_index = index
                    if position.move_stop_to_breakeven_on_partial:
                        position.stop_loss = min(position.stop_loss, position.entry_price)

                take_profit_half = position.entry_price - (position.entry_price - position.take_profit) * 0.5
                if position.trail_atr_multiple is not None and low <= take_profit_half and atr > 0:
                    position.stop_loss = min(position.stop_loss, close + atr * position.trail_atr_multiple)

                if low <= position.take_profit:
                    return self._close_position(position, index, position.take_profit, 'TP_HIT', df)
                if high >= position.stop_loss:
                    reason = 'TRAIL' if position.partial_taken and position.stop_loss <= position.entry_price else 'SL_HIT'
                    return self._close_position(position, index, position.stop_loss, reason, df)

            position.last_processed_index = index
            if index >= timeout_index:
                return self._close_position(position, index, close, 'TIMEOUT', df)

        return None

    def _close_position(self, position: PaperPosition, index: int, final_exit_price: float, reason: str, df: pd.DataFrame) -> dict:
        if position.partial_taken and position.partial_exit_price is not None:
            effective_exit = position.partial_close_fraction * position.partial_exit_price + (1 - position.partial_close_fraction) * final_exit_price
            reason = f'PARTIAL_TP+{reason}'
        else:
            effective_exit = final_exit_price

        if position.side == 'LONG':
            pnl_currency = position.position_size * (effective_exit - position.entry_price)
            pnl_pct = (effective_exit - position.entry_price) / position.entry_price * 100
        else:
            pnl_currency = position.position_size * (position.entry_price - effective_exit)
            pnl_pct = (position.entry_price - effective_exit) / position.entry_price * 100

        self.risk_manager.register_trade(pnl_currency)
        event = {
            'type': 'CLOSE',
            'position_id': position.position_id,
            'strategy': position.strategy,
            'side': position.side,
            'entry_time': position.entry_time,
            'exit_time': df.index[index].isoformat(),
            'entry_price': position.entry_price,
            'exit_price': effective_exit,
            'exit_reason': reason,
            'pnl_currency': pnl_currency,
            'pnl_pct': pnl_pct,
            'equity_after': self.risk_manager.balance,
        }
        self.events.append(event)
        return event

    def _append_journal(self, journal_path: str | Path) -> None:
        if not self.events:
            return
        path = Path(journal_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a', encoding='utf-8') as handle:
            for event in self.events:
                handle.write(json.dumps(event) + '\n')


def load_data_frame(data_path: str | Path) -> pd.DataFrame:
    return load_ohlcv_csv(data_path)
