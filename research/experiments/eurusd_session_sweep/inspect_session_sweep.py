#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

from xauusd_trading.data.loader import load_ohlcv_csv
from xauusd_trading.strategies.eurusd_session_sweep import EURUSDSessionSweepFVGStrategy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Inspect EURUSD session sweep v1 candidate setups')
    parser.add_argument('--data', required=True, help='Path to execution-timeframe OHLCV CSV')
    parser.add_argument('--limit', type=int, default=20, help='Maximum candidate signals to print')
    parser.add_argument('--execution-timeframe', default=None, help='Optional label override, e.g. M5 or M3')
    parser.add_argument('--json', action='store_true')
    return parser


def infer_execution_timeframe(path: str, override: str | None) -> str:
    if override:
        return override.upper()
    upper_path = path.upper()
    if '_M3_' in upper_path:
        return 'M3'
    if '_M5_' in upper_path:
        return 'M5'
    if '_M15_' in upper_path:
        return 'M15'
    return 'M5'


def main() -> int:
    args = build_parser().parse_args()
    df = load_ohlcv_csv(args.data)
    strategy = EURUSDSessionSweepFVGStrategy(execution_timeframe=infer_execution_timeframe(args.data, args.execution_timeframe))
    feature_df = strategy.prepare_features(df)

    signals = []
    for index in range(len(feature_df) - 1):
        signal = strategy.generate_signal(feature_df, index)
        if signal is None:
            continue
        signals.append(
            {
                'timestamp': signal.timestamp.isoformat(),
                'side': signal.side,
                'entry_price': signal.entry_price,
                'stop_loss': signal.stop_loss,
                'take_profit': signal.take_profit,
                'metadata': signal.metadata,
            }
        )
        if len(signals) >= args.limit:
            break

    payload = {
        'strategy': strategy.name,
        'data_path': args.data,
        'rows': len(feature_df),
        'trade_window_rows': int(feature_df['is_trade_window'].sum()),
        'asia_sweep_high_rows': int(feature_df['swept_asia_high'].sum()),
        'asia_sweep_low_rows': int(feature_df['swept_asia_low'].sum()),
        'sample_signals': signals,
    }

    if args.json:
        print(json.dumps(payload, indent=2, default=str))
    else:
        print(json.dumps(payload, indent=2, default=str))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
