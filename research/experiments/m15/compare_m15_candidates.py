#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

from xauusd_trading.backtesting.engine import BacktestConfig, BacktestEngine
from xauusd_trading.data.loader import load_ohlcv_csv
from xauusd_trading.reporting.metrics import summarize_trades
from xauusd_trading.risk.manager import RiskConfig
from xauusd_trading.strategies.m15_sr_sd import SRSDM15LongResearchStrategy, SRSDM15ShortResearchStrategy
from xauusd_trading.strategies.sr_sd_v35 import SRSDV35LongStrategy
from xauusd_trading.strategies.sr_sd_v35_short import SRSDV35ShortStrategy

DATA_PATH = Path('/root/.openclaw/media/inbound/xauusd_tradingbot_extracted/data/xauusd_m15_converted.csv')
OUTPUT_DIR = PROJECT_ROOT.parents[1] / 'data' / 'xauusd' / 'results' / 'm15_initial_research'


def run_strategy(df, strategy):
    engine = BacktestEngine(
        BacktestConfig(
            risk=RiskConfig(
                risk_per_trade=0.01,
                max_drawdown_pct=15.0,
                max_consecutive_losses=999,
                min_balance=1000.0,
            ),
            max_open_positions=1,
        )
    )
    trades = engine.run(df, strategy)
    summary = summarize_trades(trades)
    summary['risk_halt_reason'] = engine.last_risk_summary.get('halt_reason')
    return summary


def main() -> int:
    df = load_ohlcv_csv(DATA_PATH)
    candidates = {
        'm15_long_research': SRSDM15LongResearchStrategy(),
        'm15_short_research': SRSDM15ShortResearchStrategy(),
        'm15_long_base_like_h1': SRSDV35LongStrategy(min_rr=2.0, max_spread=300.0, warmup_bars=400, max_bars_hold=96, trail_atr_multiple=1.0, partial_tp_rr=1.0),
        'm15_short_base_like_h1': SRSDV35ShortStrategy(min_rr=2.5, max_spread=300.0, warmup_bars=400, max_bars_hold=96, trail_atr_multiple=1.2, partial_tp_rr=1.0),
    }
    summary = {name: run_strategy(df, strategy) for name, strategy in candidates.items()}

    windows = {
        '2022_2023': ('2022-01-01', '2023-12-31 23:59:59'),
        '2024_2025': ('2024-01-01', '2025-12-31 23:59:59'),
        '2025_2026': ('2025-01-01', '2026-12-31 23:59:59'),
        '2022_2024': ('2022-01-01', '2024-12-31 23:59:59'),
    }
    splits = {}
    for window_name, (start, end) in windows.items():
        window_df = df.loc[start:end].copy()
        splits[window_name] = run_strategy(window_df, SRSDM15LongResearchStrategy())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        'data_path': str(DATA_PATH),
        'summary': summary,
        'splits': splits,
    }
    out_path = OUTPUT_DIR / 'summary.json'
    out_path.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))
    print(f'Wrote: {out_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
