# Session Basket Backtest — TUNED CONFIG
**Date:** 2026-05-05 09:42
**Data:** HFM M5, Jan–May 2026
**Initial Balance:** $10,000.00
**Entry:** Next-bar open + spread | SL-first | No look-ahead

## Per-Branch Results

### eurusd_sweep
- **Pair:** EURUSD
- **Strategy:** eurusd_sweep
- **Trades:** 29 (LONG 14, SHORT 15)
- **Win Rate:** 37.9%
- **Profit Factor:** 0.88
- **Total Return:** -15.90%
- **Ending Balance:** $8,409.80
- **Max Drawdown:** 31.47%
- **Exit Reasons:** {'SL_HIT': 16, 'TIMEOUT': 10, 'TP_HIT': 3}

### eurusd_orb
- **Pair:** EURUSD
- **Strategy:** eurusd_orb
- **Trades:** 10 (LONG 6, SHORT 4)
- **Win Rate:** 30.0%
- **Profit Factor:** 0.89
- **Total Return:** -3.12%
- **Ending Balance:** $9,687.76
- **Max Drawdown:** 21.04%
- **Exit Reasons:** {'TIMEOUT': 1, 'TP_HIT': 2, 'SL_HIT': 7}

### xauusd_continuation
- **Pair:** XAUUSD
- **Strategy:** xauusd_continuation
- **Trades:** 1 (LONG 0, SHORT 1)
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Total Return:** -75.03%
- **Ending Balance:** $2,497.00
- **Max Drawdown:** 75.03%
- **Exit Reasons:** {'SL_HIT': 1}

## Basket Combined

- **Accepted:** 39 | Rejected: 1
- **Trades per Pair:** {'EURUSD': 38, 'XAUUSD': 1}
- **Trades per Branch:** {'eurusd_orb': 10, 'xauusd_continuation': 1, 'eurusd_sweep': 28}
- **Win Rate:** 35.9%
- **Profit Factor:** 0.63
- **Total Return:** -15.90%
- **Max Drawdown:** 79.65%
