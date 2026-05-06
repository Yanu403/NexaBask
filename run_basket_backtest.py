#!/usr/bin/env python3
"""Run session basket backtest with TUNED parameters on HFM data.

Active branches (PF > 0.5 from tuning):
- eurusd_sweep (s_r3 config)
- eurusd_orb (o_r1 config)
- xauusd_continuation (xau_c2 config)

Disabled branches (not viable on M5):
- eurusd_continuation (FVG too small for M5)
- gbpusd_sweep (PF 0.50)
- gbpusd_continuation (FVG too small for M5)
"""
from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd
from xauusd_trading.backtesting.engine import BacktestEngine, BacktestConfig
from xauusd_trading.data.loader import load_ohlcv_csv
from xauusd_trading.reporting.metrics import summarize_trades
from xauusd_trading.risk.manager import RiskConfig
from xauusd_trading.strategies.eurusd_session_sweep import EURUSDSessionSweepFVGStrategy
from xauusd_trading.strategies.session_continuation import SessionContinuationFVGStrategy
from xauusd_trading.strategies.session_orb_retest import SessionORBRetestStrategy

DATA_DIR = Path("/root/data/dataset_hfm")
INITIAL_BALANCE = 10_000.0

# ─── Tuned Branch Definitions ────────────────────────────────────────
BRANCHES = {
    "eurusd_sweep": {
        "pair": "EURUSD",
        "file": "EURUSDc_M5_202601050000_202605040925.csv",
        "strategy_factory": lambda: EURUSDSessionSweepFVGStrategy(
            name="eurusd_sweep",
            max_spread_pips=4.0,
            min_sweep_pips=1.0,
            min_fvg_pips=0.3,
            min_asia_range_pips=2.0,
            max_asia_range_pips=200,
            sweep_lookback_bars=60,
            entry_expiry_bars=24,
            displacement_atr_multiple=0.7,
            stop_buffer_pips=2.0,
        ),
        "risk_pct": 1.00,
        "priority": 1,
    },
    "eurusd_orb": {
        "pair": "EURUSD",
        "file": "EURUSDc_M5_202601050000_202605040925.csv",
        "strategy_factory": lambda: SessionORBRetestStrategy(
            name="eurusd_orb",
            max_spread_pips=3.0,
            breakout_buffer_pips=0.5,
            retest_tolerance_pips=1.0,
            displacement_atr_multiple=1.0,
            breakout_lookback_bars=16,
            entry_expiry_bars=12,
            stop_buffer_pips=1.0,
        ),
        "risk_pct": 0.50,
        "priority": 2,
    },
    "xauusd_continuation": {
        "pair": "XAUUSD",
        "file": "XAUUSDc_M5_202601050100_202605040930.csv",
        "strategy_factory": lambda: SessionContinuationFVGStrategy(
            name="xauusd_continuation",
            pip_size=0.01,
            spread_points_per_pip=100.0,
            max_spread_pips=10.0,
            min_fvg_pips=0.03,
            impulse_lookback_bars=48,
            entry_expiry_bars=18,
            displacement_atr_multiple=0.8,
            stop_buffer_pips=20.0,
        ),
        "risk_pct": 0.75,
        "priority": 3,
        "min_risk_distance_pips": 30.0,  # XAUUSD-specific
    },
}


def run_single_branch(branch_id: str, branch_cfg: dict) -> dict:
    csv_path = DATA_DIR / branch_cfg["file"]
    print(f"  Loading {branch_cfg['pair']} M5 from {csv_path.name}...", end=" ", flush=True)
    df = load_ohlcv_csv(csv_path)
    print(f"{len(df)} bars")

    strategy = branch_cfg["strategy_factory"]()
    min_risk = branch_cfg.get("min_risk_distance_pips", 3.0)
    risk_cfg = RiskConfig(risk_per_trade=branch_cfg["risk_pct"], max_drawdown_pct=30.0, min_risk_distance_pips=min_risk)
    bt_cfg = BacktestConfig(initial_balance=INITIAL_BALANCE, risk=risk_cfg)
    engine = BacktestEngine(config=bt_cfg)

    print(f"  Running backtest for {branch_id}...", end=" ", flush=True)
    trades = engine.run(df, strategy)
    metrics = summarize_trades(trades, initial_balance=INITIAL_BALANCE)
    print(f"{len(trades)} trades")

    long_trades = [t for t in trades if t.side == "LONG"]
    short_trades = [t for t in trades if t.side == "SHORT"]
    long_wins = [t for t in long_trades if t.pnl_currency > 0]
    short_wins = [t for t in short_trades if t.pnl_currency > 0]

    exit_reasons = {}
    for t in trades:
        r = t.exit_reason
        exit_reasons[r] = exit_reasons.get(r, 0) + 1

    return {
        "branch_id": branch_id,
        "pair": branch_cfg["pair"],
        "strategy_name": strategy.name,
        "trades": trades,
        "metrics": metrics,
        "long_count": len(long_trades),
        "short_count": len(short_trades),
        "long_wins": len(long_wins),
        "short_wins": len(short_wins),
        "exit_reasons": exit_reasons,
        "risk_summary": engine.last_risk_summary,
    }


def run_basket_combined(results: dict[str, dict]) -> dict:
    all_trades = []
    for branch_id, res in results.items():
        for t in res["trades"]:
            all_trades.append({
                "trade": t,
                "branch_id": branch_id,
                "pair": results[branch_id]["pair"],
                "priority": BRANCHES[branch_id]["priority"],
            })

    all_trades.sort(key=lambda x: x["trade"].entry_time)

    accepted = []
    symbol_occupied_until = {}

    for entry in all_trades:
        t = entry["trade"]
        pair = entry["pair"]
        occupied_until = symbol_occupied_until.get(pair)
        if occupied_until is not None and t.entry_time < occupied_until:
            continue
        accepted.append(entry)
        symbol_occupied_until[pair] = t.exit_time

    accepted_trades = [e["trade"] for e in accepted]
    basket_metrics = summarize_trades(accepted_trades, initial_balance=INITIAL_BALANCE)

    rejected = len(all_trades) - len(accepted)
    pair_counts = {}
    for e in accepted:
        p = e["pair"]
        pair_counts[p] = pair_counts.get(p, 0) + 1
    branch_counts = {}
    for e in accepted:
        b = e["branch_id"]
        branch_counts[b] = branch_counts.get(b, 0) + 1

    return {
        "metrics": basket_metrics,
        "total_accepted": len(accepted),
        "total_rejected": rejected,
        "pair_counts": pair_counts,
        "branch_counts": branch_counts,
    }


def format_report(per_branch: dict[str, dict], basket: dict) -> str:
    lines = []
    lines.append("# Session Basket Backtest — TUNED CONFIG")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Data:** HFM M5, Jan–May 2026")
    lines.append(f"**Initial Balance:** ${INITIAL_BALANCE:,.2f}")
    lines.append(f"**Entry:** Next-bar open + spread | SL-first | No look-ahead")
    lines.append("")

    lines.append("## Per-Branch Results")
    lines.append("")
    for bid, res in per_branch.items():
        m = res["metrics"]
        lines.append(f"### {bid}")
        lines.append(f"- **Pair:** {res['pair']}")
        lines.append(f"- **Strategy:** {res['strategy_name']}")
        lines.append(f"- **Trades:** {int(m['trades'])} (LONG {res['long_count']}, SHORT {res['short_count']})")
        lines.append(f"- **Win Rate:** {m['win_rate_pct']:.1f}%")
        lines.append(f"- **Profit Factor:** {m['profit_factor']:.2f}")
        lines.append(f"- **Total Return:** {m['total_return_pct']:.2f}%")
        lines.append(f"- **Ending Balance:** ${m['ending_balance']:,.2f}")
        lines.append(f"- **Max Drawdown:** {m['max_drawdown_pct']:.2f}%")
        lines.append(f"- **Exit Reasons:** {res['exit_reasons']}")
        lines.append("")

    lines.append("## Basket Combined")
    lines.append("")
    bm = basket["metrics"]
    lines.append(f"- **Accepted:** {basket['total_accepted']} | Rejected: {basket['total_rejected']}")
    lines.append(f"- **Trades per Pair:** {basket['pair_counts']}")
    lines.append(f"- **Trades per Branch:** {basket['branch_counts']}")
    lines.append(f"- **Win Rate:** {bm['win_rate_pct']:.1f}%")
    lines.append(f"- **Profit Factor:** {bm['profit_factor']:.2f}")
    lines.append(f"- **Total Return:** {bm['total_return_pct']:.2f}%")
    lines.append(f"- **Max Drawdown:** {bm['max_drawdown_pct']:.2f}%")
    lines.append("")

    return "\n".join(lines)


def main():
    print("=" * 60)
    print("TUNED SESSION BASKET BACKTEST")
    print("Entry: next-bar open + spread | SL-first | No look-ahead")
    print("=" * 60)
    print()

    per_branch = {}
    for branch_id, cfg in BRANCHES.items():
        print(f"[{branch_id}]")
        result = run_single_branch(branch_id, cfg)
        m = result["metrics"]
        print(f"  → {int(m['trades'])} trades | WR {m['win_rate_pct']:.1f}% | PF {m['profit_factor']:.2f} | Return {m['total_return_pct']:.2f}% | DD {m['max_drawdown_pct']:.2f}%")
        per_branch[branch_id] = result
        print()

    print("Computing basket...")
    basket = run_basket_combined(per_branch)
    bm = basket["metrics"]
    print(f"  → {basket['total_accepted']} accepted, {basket['total_rejected']} rejected")
    print(f"  → WR {bm['win_rate_pct']:.1f}% | PF {bm['profit_factor']:.2f} | Return {bm['total_return_pct']:.2f}% | DD {bm['max_drawdown_pct']:.2f}%")
    print()

    report = format_report(per_branch, basket)
    report_path = Path(__file__).parent / "docs" / f"backtest_tuned_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
