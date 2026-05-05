# Session Basket Backtest Report
**Date:** 2026-05-05 07:24
**Data:** HFM M5, Jan–May 2026
**Initial Balance:** $10,000.00
**Entry Model:** Next-bar open + spread (conservative)
**Same-bar Ambiguity:** SL-first (conservative)
**Swing Detection:** Backward-only (no look-ahead bias)

## Per-Branch Results

### eurusd_sweep
- **Pair:** EURUSD
- **Strategy:** eurusd_sweep
- **Trades:** 1 (LONG 1, SHORT 0)
- **LONG win rate:** 0.0% (0/1)
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Total Return:** -21.41%
- **Ending Balance:** $7,859.14
- **Max Drawdown:** 21.41%
- **Avg Win:** 0.0000%
- **Avg Loss:** -0.1437%
- **Exit Reasons:** {'SL_HIT': 1}

### eurusd_continuation
- **Pair:** EURUSD
- **Strategy:** eurusd_continuation
- **Trades:** 0 (LONG 0, SHORT 0)
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Total Return:** 0.00%
- **Ending Balance:** $10,000.00
- **Max Drawdown:** 0.00%
- **Avg Win:** 0.0000%
- **Avg Loss:** 0.0000%
- **Exit Reasons:** {}

### eurusd_orb
- **Pair:** EURUSD
- **Strategy:** eurusd_orb
- **Trades:** 8 (LONG 1, SHORT 7)
- **LONG win rate:** 0.0% (0/1)
- **SHORT win rate:** 42.9% (3/7)
- **Win Rate:** 37.5%
- **Profit Factor:** 0.99
- **Total Return:** -0.23%
- **Ending Balance:** $9,976.52
- **Max Drawdown:** 24.00%
- **Avg Win:** 0.0820%
- **Avg Loss:** -0.0336%
- **Exit Reasons:** {'TP_HIT': 3, 'SL_HIT': 5}

### gbpusd_sweep
- **Pair:** GBPUSD
- **Strategy:** gbpusd_sweep
- **Trades:** 1 (LONG 1, SHORT 0)
- **LONG win rate:** 0.0% (0/1)
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Total Return:** -36.11%
- **Ending Balance:** $6,388.56
- **Max Drawdown:** 36.11%
- **Avg Win:** 0.0000%
- **Avg Loss:** -0.2287%
- **Exit Reasons:** {'SL_HIT': 1}

### gbpusd_continuation
- **Pair:** GBPUSD
- **Strategy:** gbpusd_continuation
- **Trades:** 0 (LONG 0, SHORT 0)
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Total Return:** 0.00%
- **Ending Balance:** $10,000.00
- **Max Drawdown:** 0.00%
- **Avg Win:** 0.0000%
- **Avg Loss:** 0.0000%
- **Exit Reasons:** {}

### xauusd_continuation
- **Pair:** XAUUSD
- **Strategy:** xauusd_continuation
- **Trades:** 1 (LONG 0, SHORT 1)
- **SHORT win rate:** 0.0% (0/1)
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Total Return:** -75.03%
- **Ending Balance:** $2,497.00
- **Max Drawdown:** 75.03%
- **Avg Win:** 0.0000%
- **Avg Loss:** 0.0000%
- **Exit Reasons:** {'SL_HIT': 1}

## Basket Combined (One-Position-Per-Symbol)

- **Total Accepted Trades:** 11
- **Rejected (conflicts):** 0
- **Trades per Pair:** {'EURUSD': 9, 'XAUUSD': 1, 'GBPUSD': 1}
- **Trades per Branch:** {'eurusd_orb': 8, 'xauusd_continuation': 1, 'eurusd_sweep': 1, 'gbpusd_sweep': 1}
- **Win Rate:** 27.3%
- **Profit Factor:** 0.25
- **Total Return:** -0.23%
- **Ending Balance:** $9,976.52
- **Max Drawdown:** 77.66%

## Risk Summary (Per Branch)

### eurusd_sweep
- balance: 7859.143999999969
- peak_balance: 10000.0
- current_drawdown_pct: 21.408560000000307
- max_drawdown_seen_pct: 21.408560000000307
- consecutive_losses: 1
- halt_reason: MAX_DRAWDOWN_BREACH

### eurusd_continuation
- balance: 10000.0
- peak_balance: 10000.0
- current_drawdown_pct: 0.0
- max_drawdown_seen_pct: 0.0
- consecutive_losses: 0
- halt_reason: None

### eurusd_orb
- balance: 9976.519999999866
- peak_balance: 13127.780000000297
- current_drawdown_pct: 24.004515614981056
- max_drawdown_seen_pct: 24.004515614981056
- consecutive_losses: 3
- halt_reason: MAX_DRAWDOWN_BREACH

### gbpusd_sweep
- balance: 6388.55600000011
- peak_balance: 10000.0
- current_drawdown_pct: 36.11443999999891
- max_drawdown_seen_pct: 36.11443999999891
- consecutive_losses: 1
- halt_reason: MAX_DRAWDOWN_BREACH

### gbpusd_continuation
- balance: 10000.0
- peak_balance: 10000.0
- current_drawdown_pct: 0.0
- max_drawdown_seen_pct: 0.0
- consecutive_losses: 0
- halt_reason: None

### xauusd_continuation
- balance: 2497.0
- peak_balance: 10000.0
- current_drawdown_pct: 75.03
- max_drawdown_seen_pct: 75.03
- consecutive_losses: 1
- halt_reason: MAX_DRAWDOWN_BREACH
