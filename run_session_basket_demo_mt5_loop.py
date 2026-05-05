#!/usr/bin/env python3
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

    while True:
        iteration += 1
        payload = run_once(args)
        per_symbol = payload.get('per_symbol', {})
        open_positions = sum(len(item.get('open_positions', [])) for item in per_symbol.values())
        event_count = sum(int(item.get('event_count', 0)) for item in per_symbol.values())
        accepted_count = len(payload.get('accepted_signals', []))
        rejected_count = len(payload.get('rejected_signals', []))
        telegram_sent = int(payload.get('telegram_alerts_sent', 0))

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
            print(
                f"[{heartbeat['timestamp']}] iter={iteration} "
                f"accepted={accepted_count} rejected={rejected_count} open={open_positions} "
                f"events={event_count} telegram={telegram_sent} debug={heartbeat['debug_summary']}"
            )

        if args.max_iterations and iteration >= args.max_iterations:
            break
        time.sleep(max(args.interval_seconds, 1))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
