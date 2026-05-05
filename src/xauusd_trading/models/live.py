from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from typing import Any

from xauusd_trading.models.trading import _VALID_SIDES, _check_finite

_VALID_ACTIONS: frozenset[str] = frozenset({"HOLD", "OPEN", "REVERSE", "SYNC_SLTP", "MANAGE_POSITION"})


@dataclass(slots=True)
class BrokerPosition:
    ticket: int
    symbol: str
    side: str
    volume: float
    price_open: float
    stop_loss: float
    take_profit: float
    price_current: float
    profit: float
    magic: int | None = None
    comment: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class OrderIntent:
    symbol: str
    side: str
    volume: float
    entry_price: float
    stop_loss: float
    take_profit: float
    deviation: int = 20
    magic: int = 35042026
    comment: str = "xauusd_trading_bot"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.side not in _VALID_SIDES:
            raise ValueError(f"side must be 'LONG' or 'SHORT', got {self.side!r}")
        if self.volume <= 0:
            raise ValueError(f"volume must be > 0, got {self.volume}")
        for _name in ("volume", "entry_price", "stop_loss", "take_profit"):
            _check_finite(getattr(self, _name), _name)
        if len(self.comment) > 31:
            raise ValueError(
                f"MT5 comment must be ≤ 31 chars, got {len(self.comment)}: {self.comment!r}"
            )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PositionSyncPlan:
    ticket: int
    symbol: str
    target_stop_loss: float
    target_take_profit: float
    current_stop_loss: float
    current_take_profit: float
    side: str
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PositionManagementPlan:
    ticket: int
    symbol: str
    side: str
    current_volume: float
    partial_close_volume: float = 0.0
    partial_close_reason: str | None = None
    sync_plan: PositionSyncPlan | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ExecutionDecision:
    action: str
    reason: str
    intent: OrderIntent | None = None
    broker_positions: list[BrokerPosition] = field(default_factory=list)
    sync_plan: PositionSyncPlan | None = None
    management_plan: PositionManagementPlan | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.action not in _VALID_ACTIONS:
            raise ValueError(
                f"action must be one of {sorted(_VALID_ACTIONS)}, got {self.action!r}"
            )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
