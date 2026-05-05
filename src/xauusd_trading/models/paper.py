from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from typing import Any

from xauusd_trading.models.trading import _VALID_SIDES, _check_finite


@dataclass(slots=True)
class PaperPosition:
    position_id: str
    strategy: str
    side: str
    entry_index: int
    last_processed_index: int
    entry_time: str
    entry_price: float
    stop_loss: float
    take_profit: float
    max_hold_bars: int
    position_size: float
    risk_amount: float
    trail_atr_multiple: float | None = None
    partial_tp_rr: float | None = None
    partial_close_fraction: float = 0.5
    move_stop_to_breakeven_on_partial: bool = True
    partial_taken: bool = False
    partial_exit_price: float | None = None
    partial_exit_index: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.side not in _VALID_SIDES:
            raise ValueError(f"side must be 'LONG' or 'SHORT', got {self.side!r}")
        if self.entry_price <= 0:
            raise ValueError(f"entry_price must be > 0, got {self.entry_price}")
        if self.position_size <= 0:
            raise ValueError(f"position_size must be > 0, got {self.position_size}")
        for _name in ("entry_price", "stop_loss", "take_profit", "position_size", "risk_amount"):
            _check_finite(getattr(self, _name), _name)
        if not (0.0 < self.partial_close_fraction <= 1.0):
            raise ValueError(
                f"partial_close_fraction must be in (0, 1], got {self.partial_close_fraction}"
            )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PaperState:
    generated_at: str
    data_path: str
    balance: float
    peak_balance: float
    closed_trades: int
    open_positions: list[PaperPosition] = field(default_factory=list)
    journal_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload['open_positions'] = [position.to_dict() for position in self.open_positions]
        return payload
