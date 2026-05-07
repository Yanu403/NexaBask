#!/usr/bin/env python3
"""Periodic MT5 demo basket scheduler for session portfolio v1.

Outputs a beautiful terminal dashboard instead of raw JSON.
Use --json for machine-readable output.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

from run_session_basket_demo_mt5 import build_parser as build_single_parser
from run_session_basket_demo_mt5 import run_once
from xauusd_trading.execution.terminal_ui import (
    BANNER,
    format_heartbeat,
    format_signal_event,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_parser() -> argparse.ArgumentParser:
    parent = build_single_parser(add_help=False)
    parser = argparse.ArgumentParser(
        description='Periodic MT5 demo basket scheduler for session portfolio v1',
        parents=[parent],
        add_help=True,
    )
    parser.add_argument('--interval-seconds', type=int, default=180)
    parser.add_argument('--max-iterations', type=int, default=0, help='0 means run forever')
    parser.add_argument('--heartbeat-log', default=str(PROJECT_ROOT / 'runtime' / 'session_basket_demo_loop.jsonl'))
    return parser


def append_heartbeat(path: str | Path, payload: dict) -> None:
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(payload) + '\n')


def main() -> int:
    args = build_parser().parse_args()
    iteration = 0

    # Startup banner
    if not args.json:
        print(BANNER)
        print(f"  Loop: every {args.interval_seconds}s  │  Press Ctrl+C to stop")
        print()

    while True:
        iteration += 1
        payload = run_once(args)
        per_symbol = payload.get('per_symbol', {})
        open_positions = sum(len(item.get('open_positions', [])) for item in per_symbol.values())
        event_count = sum(int(item.get('event_count', 0)) for item in per_symbol.values())
        accepted_count = len(payload.get('accepted_signals', []))
        rejected_count = len(payload.get('rejected_signals', []))
        telegram_sent = int(payload.get('telegram_alerts_sent', 0))
        branch_debugs = payload.get('branch_debugs', [])

        # Extract balance info from first symbol that has it
        balance = None
        peak_balance = None
        closed_trades = None
        for sym, info in per_symbol.items():
            if info.get('balance') is not None:
                balance = info.get('balance')
                peak_balance = info.get('peak_balance')
                closed_trades = info.get('closed_trades', 0)
                break

        heartbeat = {
            'timestamp': utc_now(),
            'iteration': iteration,
            'accepted_signals': accepted_count,
            'rejected_signals': rejected_count,
            'open_positions': open_positions,
            'event_count': event_count,
            'telegram_alerts_sent': telegram_sent,
            'debug_summary': payload.get('debug_summary', 'none'),
            'symbols': {
                symbol: {
                    'open_positions': len(item.get('open_positions', [])),
                    'closed_trades': item.get('closed_trades'),
                    'latest_bar_time': item.get('latest_bar_time'),
                }
                for symbol, item in per_symbol.items()
            },
        }

        append_heartbeat(args.heartbeat_log, heartbeat)

        if args.json:
            print(json.dumps({'heartbeat': heartbeat, 'payload': payload}, indent=2))
        else:
            # Beautiful dashboard output
            print(format_heartbeat(
                iteration=iteration,
                timestamp=heartbeat['timestamp'],
                mode='DEMO',
                accepted=accepted_count,
                rejected=rejected_count,
                open_positions=open_positions,
                telegram_sent=telegram_sent,
                debug_summary=heartbeat['debug_summary'],
                branch_debugs=branch_debugs,
                balance=balance,
                peak_balance=peak_balance,
                closed_trades=closed_trades,
            ))

            # Show events (trades opened/closed) with nice formatting
            for sym, info in per_symbol.items():
                for event in info.get('events', []):
                    print(format_signal_event(event))

            print()  # blank line between iterations

        if args.max_iterations and iteration >= args.max_iterations:
            break
        time.sleep(max(args.interval_seconds, 1))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
