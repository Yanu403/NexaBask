"""Core dataclasses used across strategy, backtest, and execution layers."""

from xauusd_trading.models.trading import Side, TradeSignal, ExecutedTrade
from xauusd_trading.models.live import (
    BrokerPosition,
    OrderIntent,
    PositionSyncPlan,
    PositionManagementPlan,
    ExecutionDecision,
)
from xauusd_trading.models.paper import PaperPosition, PaperState

__all__ = [
    "Side",
    "TradeSignal",
    "ExecutedTrade",
    "BrokerPosition",
    "OrderIntent",
    "PositionSyncPlan",
    "PositionManagementPlan",
    "ExecutionDecision",
    "PaperPosition",
    "PaperState",
]
