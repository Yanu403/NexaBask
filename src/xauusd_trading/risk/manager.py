from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RiskConfig:
    risk_per_trade: float = 0.01
    max_drawdown_pct: float = 20.0
    max_consecutive_losses: int = 6
    min_balance: float = 1_000.0
    max_position_lots: float = 10.0
    lot_size: float = 100_000.0
    min_risk_distance_pips: float = 5.0


class RiskManager:
    def __init__(self, *, initial_balance: float, config: RiskConfig | None = None) -> None:
        self.config = config or RiskConfig()
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.peak_balance = initial_balance
        self.max_drawdown_seen_pct = 0.0
        self.consecutive_losses = 0
        self.halt_reason: str | None = None

    def can_open_trade(self) -> bool:
        if self.halt_reason is not None:
            return False

        if self.balance < self.config.min_balance:
            self.halt_reason = "MIN_BALANCE_BREACH"
            return False

        drawdown_pct = self.current_drawdown_pct
        if drawdown_pct >= self.config.max_drawdown_pct:
            self.halt_reason = "MAX_DRAWDOWN_BREACH"
            return False

        if self.consecutive_losses >= self.config.max_consecutive_losses:
            self.halt_reason = "MAX_CONSECUTIVE_LOSSES"
            return False

        return True

    def size_position(self, *, entry_price: float, stop_loss: float, pip_size: float = 0.0001) -> tuple[float, float]:
        stop_distance = abs(entry_price - stop_loss)
        risk_amount = self.balance * self.config.risk_per_trade

        # Skip trades with too-tight stops (position size would blow up)
        stop_pips = stop_distance / pip_size
        if stop_pips < self.config.min_risk_distance_pips:
            return risk_amount, 0.0  # Zero size = skip this trade

        position_size = risk_amount / stop_distance if stop_distance > 0 else 0.0

        # Cap at max_position_lots
        max_units = self.config.max_position_lots * self.config.lot_size
        position_size = min(position_size, max_units)

        return risk_amount, position_size

    def register_trade(self, pnl_currency: float) -> None:
        self.balance += pnl_currency
        self.peak_balance = max(self.peak_balance, self.balance)
        self.max_drawdown_seen_pct = max(self.max_drawdown_seen_pct, self.current_drawdown_pct)

        if pnl_currency > 0:
            self.consecutive_losses = 0
        else:
            self.consecutive_losses += 1

        self.can_open_trade()

    @property
    def current_drawdown_pct(self) -> float:
        if self.peak_balance <= 0:
            return 0.0
        return max(0.0, ((self.peak_balance - self.balance) / self.peak_balance) * 100)

    def summary(self) -> dict[str, float | str | None]:
        return {
            "balance": self.balance,
            "peak_balance": self.peak_balance,
            "current_drawdown_pct": self.current_drawdown_pct,
            "max_drawdown_seen_pct": self.max_drawdown_seen_pct,
            "consecutive_losses": self.consecutive_losses,
            "halt_reason": self.halt_reason,
        }
