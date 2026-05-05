#!/usr/bin/env python3
"""Paper-trade runner using local CSV data (no MT5 required).

Reads the latest CSV data from /root/data/dataset_hfm/,
runs all tuned strategies on each symbol, and logs signals + paper trades.

Can run as a one-shot or as a background loop (cron-style).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from xauusd_trading.data.loader import load_ohlcv_csv
from xauusd_trading.strategies.eurusd_session_sweep import EURUSDSessionSweepFVGStrategy
from xauusd_trading.strategies.session_continuation import SessionContinuationFVGStrategy
from xauusd_trading.strategies.session_orb_retest import SessionORBRetestStrategy

DATA_DIR = Path("/root/data/dataset_hfm")
STATE_DIR = PROJECT_ROOT / "runtime" / "paper_states"
JOURNAL_DIR = PROJECT_ROOT / "runtime" / "paper_journals"

# ── Tuned Branch Definitions (same as MT5 runner) ────────────────────
BRANCHES = {
    "eurusd_sweep": {
        "symbol": "EURUSD",
        "file_pattern": "EURUSDc_M5_*.csv",
        "priority": 1,
        "risk_per_trade": 0.005,
        "min_risk_distance_pips": 3.0,
        "strategy_factory": lambda: EURUSDSessionSweepFVGStrategy(
            name="eurusd_sweep",
            max_spread_pips=4.0, min_sweep_pips=1.0, min_fvg_pips=0.3,
            min_asia_range_pips=2.0, max_asia_range_pips=200,
            sweep_lookback_bars=60, entry_expiry_bars=24,
            displacement_atr_multiple=0.7, stop_buffer_pips=2.0,
            pip_size=0.0001, spread_points_per_pip=10.0,
        ),
    },
    "gbpusd_orb": {
        "symbol": "GBPUSD",
        "file_pattern": "GBPUSDc_M5_*.csv",
        "priority": 2,
        "risk_per_trade": 0.003,
        "min_risk_distance_pips": 3.0,
        "strategy_factory": lambda: SessionORBRetestStrategy(
            name="gbpusd_orb",
            max_spread_pips=3.0, breakout_buffer_pips=0.5,
            retest_tolerance_pips=1.0, displacement_atr_multiple=1.0,
            breakout_lookback_bars=16, entry_expiry_bars=12,
            stop_buffer_pips=1.0,
            pip_size=0.0001, spread_points_per_pip=10.0,
        ),
    },
    "eurusd_orb": {
        "symbol": "EURUSD",
        "file_pattern": "EURUSDc_M5_*.csv",
        "priority": 3,
        "risk_per_trade": 0.003,
        "min_risk_distance_pips": 3.0,
        "strategy_factory": lambda: SessionORBRetestStrategy(
            name="eurusd_orb",
            max_spread_pips=3.0, breakout_buffer_pips=0.5,
            retest_tolerance_pips=1.0, displacement_atr_multiple=1.0,
            breakout_lookback_bars=16, entry_expiry_bars=12,
            stop_buffer_pips=1.0,
            pip_size=0.0001, spread_points_per_pip=10.0,
        ),
    },
    "xauusd_continuation": {
        "symbol": "XAUUSD",
        "file_pattern": "XAUUSDc_M5_*.csv",
        "priority": 4,
        "risk_per_trade": 0.003,
        "min_risk_distance_pips": 50.0,
        "strategy_factory": lambda: SessionContinuationFVGStrategy(
            name="xauusd_continuation",
            pip_size=0.01, spread_points_per_pip=100.0,
            max_spread_pips=10.0, min_fvg_pips=0.03,
            impulse_lookback_bars=48, entry_expiry_bars=18,
            displacement_atr_multiple=0.8, stop_buffer_pips=30.0,
        ),
    },
}


def find_latest_csv(pattern: str, data_dir: Path) -> Path | None:
    matches = sorted(data_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0] if matches else None


def run_once(args: argparse.Namespace) -> dict:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)

    results = {}
    all_signals = []

    for branch_id, cfg in BRANCHES.items():
        csv_path = find_latest_csv(cfg["file_pattern"], DATA_DIR)
        if csv_path is None:
            results[branch_id] = {"status": "NO_DATA", "file_pattern": cfg["file_pattern"]}
            continue

        try:
            df = load_ohlcv_csv(csv_path)
        except Exception as e:
            results[branch_id] = {"status": "LOAD_ERROR", "error": str(e)}
            continue

        strategy = cfg["strategy_factory"]()
        feature_df = strategy.prepare_features(df)

        # Check latest bar
        last_idx = len(feature_df) - 1
        signal = strategy.generate_signal(feature_df, last_idx)
        debug_info = strategy.debug_signal(feature_df, last_idx)

        entry = {
            "branch_id": branch_id,
            "symbol": cfg["symbol"],
            "priority": cfg["priority"],
            "risk_per_trade": cfg["risk_per_trade"],
            "data_file": csv_path.name,
            "bars": len(df),
            "latest_bar_time": str(df.index[-1]),
            "has_signal": signal is not None,
            "debug_reason": debug_info.get("reason_code", "UNKNOWN"),
            "debug_summary": debug_info.get("summary", ""),
        }

        if signal is not None:
            risk_pips = abs(signal.entry_price - signal.stop_loss) / strategy.pip_size
            entry.update({
                "side": signal.side,
                "entry_price": signal.entry_price,
                "stop_loss": signal.stop_loss,
                "take_profit": signal.take_profit,
                "risk_pips": round(risk_pips, 1),
                "rr_ratio": round(abs(signal.entry_price - signal.take_profit) / abs(signal.entry_price - signal.stop_loss), 1),
                "max_hold_bars": signal.max_hold_bars,
            })
            all_signals.append(entry)

            # Log signal to journal
            journal_path = JOURNAL_DIR / f"{branch_id}.jsonl"
            with open(journal_path, "a") as f:
                f.write(json.dumps({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    **entry,
                }) + "\n")

        results[branch_id] = entry

    # Resolve same-symbol conflicts (lower priority number wins)
    by_symbol: dict[str, list] = {}
    for sig in all_signals:
        by_symbol.setdefault(sig["symbol"], []).append(sig)
    accepted = []
    for symbol, sigs in by_symbol.items():
        sigs.sort(key=lambda s: s["priority"])
        accepted.append(sigs[0])
        for loser in sigs[1:]:
            loser["rejected_by"] = sigs[0]["branch_id"]
            loser["rejection_reason"] = "LOWER_PRIORITY_SAME_SYMBOL"

    return {
        "scan_time": datetime.now(timezone.utc).isoformat(),
        "total_branches": len(BRANCHES),
        "signals_found": len(all_signals),
        "accepted_signals": len(accepted),
        "results": results,
        "accepted": accepted,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Paper-trade scanner (no MT5 needed)")
    parser.add_argument("--loop", action="store_true", help="Run as continuous loop")
    parser.add_argument("--interval", type=int, default=300, help="Loop interval in seconds (default: 300 = 5 min)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    if args.loop:
        print(f"Starting paper-trade loop (every {args.interval}s). Ctrl+C to stop.")
        try:
            while True:
                result = run_once(args)
                now = result["scan_time"]
                sig_count = result["signals_found"]
                acc_count = result["accepted_signals"]
                print(f"[{now}] Scan complete: {sig_count} signals, {acc_count} accepted")
                for sig in result["accepted"]:
                    print(f"  ✅ {sig['branch_id']}: {sig['side']} {sig['symbol']} @ {sig['entry_price']:.5f} SL={sig['stop_loss']:.5f} TP={sig['take_profit']:.5f} R:R={sig['rr_ratio']}")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopped by user.")
        return 0

    result = run_once(args)
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"\n{'='*60}")
        print(f"PAPER TRADE SCAN — {result['scan_time']}")
        print(f"{'='*60}")
        print(f"Branches: {result['total_branches']} | Signals: {result['signals_found']} | Accepted: {result['accepted_signals']}")
        print()
        for branch_id, info in result["results"].items():
            status = "✅ SIGNAL" if info.get("has_signal") else f"❌ {info.get('debug_reason', 'NO_DATA')}"
            print(f"  {branch_id:25s} {status:20s} | {info.get('symbol', '?')} | bars={info.get('bars', '?')} | reason={info.get('debug_reason', '?')}")
        print()
        if result["accepted"]:
            print("ACCEPTED SIGNALS:")
            for sig in result["accepted"]:
                print(f"  ✅ {sig['branch_id']}: {sig['side']} {sig['symbol']} @ {sig['entry_price']:.5f}")
                print(f"     SL={sig['stop_loss']:.5f} TP={sig['take_profit']:.5f} R:R={sig['rr_ratio']} risk={sig['risk_pips']}pips")
        else:
            print("No signals accepted at this time.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
