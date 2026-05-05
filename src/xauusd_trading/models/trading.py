from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Literal

import pandas as pd

Side = Literal["LONG", "SHORT"]
_VALID_SIDES: frozenset[str] = frozenset({"LONG", "SHORT"})


def _check_finite(value: float, name: str) -> None:
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"{name} must be finite, got {value!r}")


@dataclass(slots=True)
class TradeSignal:
    index: int
    timestamp: pd.Timestamp
    side: str
    entry_price: float
    stop_loss: float
    take_profit: float
    max_hold_bars: int = 20
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.side not in _VALID_SIDES:
            raise ValueError(f"side must be 'LONG' or 'SHORT', got {self.side!r}")
        if self.entry_price <= 0:
            raise ValueError(f"entry_price must be > 0, got {self.entry_price}")
        for _name in ("entry_price", "stop_loss", "take_profit"):
            _check_finite(getattr(self, _name), _name)
        if self.side == "LONG":
            if not (self.stop_loss < self.entry_price < self.take_profit):
                raise ValueError(
                    f"LONG requires stop_loss < entry_price < take_profit, "
                    f"got SL={self.stop_loss}, entry={self.entry_price}, TP={self.take_profit}"
                )
        else:  # SHORT
            if not (self.stop_loss > self.entry_price > self.take_profit):
                raise ValueError(
                    f"SHORT requires stop_loss > entry_price > take_profit, "
                    f"got SL={self.stop_loss}, entry={self.entry_price}, TP={self.take_profit}"
                )


@dataclass(slots=True)
class ExecutedTrade:
    entry_index: int
    exit_index: int
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    side: str
    entry_price: float
    exit_price: float
    stop_loss: float
    take_profit: float
    exit_reason: str
    pnl_pct: float
    pnl_currency: float
    position_size: float
    risk_amount: float
    equity_before: float
    equity_after: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.side not in _VALID_SIDES:
            raise ValueError(f"side must be 'LONG' or 'SHORT', got {self.side!r}")
        if self.entry_price <= 0:
            raise ValueError(f"entry_price must be > 0, got {self.entry_price}")
        if self.position_size <= 0:
            raise ValueError(f"position_size must be > 0, got {self.position_size}")
        for _name in (
            "entry_price", "exit_price", "stop_loss", "take_profit",
            "pnl_pct", "pnl_currency", "position_size",
            "risk_amount", "equity_before", "equity_after",
        ):
            _check_finite(getattr(self, _name), _name)
        if self.side == "LONG":
            if not (self.stop_loss < self.entry_price < self.take_profit):
                raise ValueError(
                    f"LONG requires stop_loss < entry_price < take_profit, "
                    f"got SL={self.stop_loss}, entry={self.entry_price}, TP={self.take_profit}"
                )
        else:  # SHORT
            if not (self.stop_loss > self.entry_price > self.take_profit):
                raise ValueError(
                    f"SHORT requires stop_loss > entry_price > take_profit, "
                    f"got SL={self.stop_loss}, entry={self.entry_price}, TP={self.take_profit}"
                )
