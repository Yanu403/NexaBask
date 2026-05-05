from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

from xauusd_trading.models.trading import TradeSignal


class Strategy(ABC):
    name: str = "unnamed_strategy"

    @abstractmethod
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def generate_signal(self, df: pd.DataFrame, index: int) -> TradeSignal | None:
        raise NotImplementedError

    def debug_signal(self, df: pd.DataFrame, index: int) -> dict[str, Any]:
        signal = self.generate_signal(df, index)
        if signal is not None:
            return self._debug_signal_ready(signal)
        return self._debug_payload(False, 'NO_SIGNAL', 'No signal generated')

    def _debug_payload(
        self,
        has_signal: bool,
        reason_code: str,
        summary: str,
        *,
        side: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            'strategy': self.name,
            'has_signal': has_signal,
            'reason_code': reason_code,
            'summary': summary,
            'details': details or {},
        }
        if side is not None:
            payload['side'] = side
        return payload

    def _debug_signal_ready(self, signal: TradeSignal) -> dict[str, Any]:
        return self._debug_payload(
            True,
            'SIGNAL_READY',
            f'{signal.side} signal ready',
            side=signal.side,
            details={
                'entry_price': signal.entry_price,
                'stop_loss': signal.stop_loss,
                'take_profit': signal.take_profit,
                'timestamp': signal.timestamp.isoformat(),
            },
        )

    def _combine_side_debugs(self, side_debugs: list[dict[str, Any]]) -> dict[str, Any]:
        if not side_debugs:
            return self._debug_payload(False, 'NO_SIDE_READY', 'No side qualified')
        unique_codes = {str(item.get('reason_code', 'UNKNOWN')) for item in side_debugs}
        if len(unique_codes) == 1:
            code = str(side_debugs[0].get('reason_code', 'UNKNOWN'))
            summary = str(side_debugs[0].get('summary', code))
        else:
            code = 'NO_SIDE_READY'
            summary = ' | '.join(
                f"{item.get('side', '?')}:{item.get('reason_code', 'UNKNOWN')}" for item in side_debugs
            )
        return self._debug_payload(False, code, summary, details={'per_side': side_debugs})
