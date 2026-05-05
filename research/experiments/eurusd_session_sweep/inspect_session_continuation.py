#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

from xauusd_trading.data.loader import load_ohlcv_csv
from xauusd_trading.strategies.session_continuation import SessionContinuationFVGStrategy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Inspect session continuation v1 candidate setups')
    parser.add_argument('--data', required=True)
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--json', action='store_true')
    return parser


def infer_execution_timeframe(path: str) -> str:
    upper = path.upper()
    if '_M3_' in upper:
        return 'M3'
    if '_M5_' in upper:
        return 'M5'
    if '_M15_' in upper:
        return 'M15'
    return 'M3'


def main() -> int:
    args = build_parser().parse_args()
    df = load_ohlcv_csv(args.data)
    strategy = SessionContinuationFVGStrategy(execution_timeframe=infer_execution_timeframe(args.data))
    feature_df = strategy.prepare_features(df)
    signals = []
    for index in range(len(feature_df) - 1):
        signal = strategy.generate_signal(feature_df, index)
        if signal is None:
            continue
        signals.append({
            'timestamp': signal.timestamp.isoformat(),
            'side': signal.side,
            'entry_price': signal.entry_price,
            'stop_loss': signal.stop_loss,
            'take_profit': signal.take_profit,
            'metadata': signal.metadata,
        })
        if len(signals) >= args.limit:
            break
    payload = {
        'strategy': strategy.name,
        'data_path': args.data,
        'rows': len(feature_df),
        'trade_window_rows': int(feature_df['is_trade_window'].sum()),
        'bullish_displacement_rows': int(feature_df['bullish_displacement'].sum()),
        'bearish_displacement_rows': int(feature_df['bearish_displacement'].sum()),
        'sample_signals': signals,
    }
    print(json.dumps(payload, indent=2, default=str))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
