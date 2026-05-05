from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from xauusd_trading.models.trading import TradeSignal
from xauusd_trading.strategies.base import Strategy


@dataclass(slots=True)
class PortfolioDecision:
    signals: list[TradeSignal]
    latest_index: int
    strategy_debugs: list[dict] = field(default_factory=list)


def compact_debug_summary(debugs: list[dict], *, limit: int = 3) -> str:
    if not debugs:
        return 'none'
    parts: list[str] = []
    for item in debugs[:limit]:
        label = str(item.get('branch_id') or item.get('strategy') or item.get('symbol') or 'unknown')
        code = str(item.get('reason_code') or 'UNKNOWN')
        side = item.get('side')
        if side and code != 'SIGNAL_READY':
            parts.append(f'{label}:{side}:{code}')
        else:
            parts.append(f'{label}:{code}')
    if len(debugs) > limit:
        parts.append(f'+{len(debugs) - limit} more')
    return ', '.join(parts)


def collect_portfolio_signals(df: pd.DataFrame, strategies: list[Strategy]) -> PortfolioDecision:
    latest_index = len(df) - 1
    signals: list[TradeSignal] = []
    strategy_debugs: list[dict] = []
    for priority, strategy in enumerate(strategies, start=1):
        feature_df = strategy.prepare_features(df)
        signal = strategy.generate_signal(feature_df, latest_index)
        debug_info = dict(strategy.debug_signal(feature_df, latest_index))
        debug_info['strategy_priority'] = priority
        strategy_debugs.append(debug_info)
        if signal is None:
            continue
        signal.metadata['strategy_priority'] = priority
        signals.append(signal)
    return PortfolioDecision(signals=signals, latest_index=latest_index, strategy_debugs=strategy_debugs)
