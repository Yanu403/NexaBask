# Session Basket Backtest Report
**Date:** 2026-05-05 06:59
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
- **Total Return:** -107.99%
- **Ending Balance:** $-798.71
- **Max Drawdown:** 107.99%
- **Avg Win:** 0.0000%
- **Avg Loss:** -0.1583%
- **Exit Reasons:** {'SL_HIT': 1}

### eurusd_continuation
- **Pair:** EURUSD
- **Strategy:** eurusd_continuation
- **Trades:** 1 (LONG 0, SHORT 1)
- **SHORT win rate:** 0.0% (0/1)
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Total Return:** -162.56%
- **Ending Balance:** $-6,256.50
- **Max Drawdown:** 162.56%
- **Avg Win:** 0.0000%
- **Avg Loss:** 0.0000%
- **Exit Reasons:** {'SL_HIT': 1}

### eurusd_orb
- **Pair:** EURUSD
- **Strategy:** eurusd_orb
- **Trades:** 2 (LONG 1, SHORT 1)
- **LONG win rate:** 0.0% (0/1)
- **SHORT win rate:** 100.0% (1/1)
- **Win Rate:** 50.0%
- **Profit Factor:** 0.48
- **Total Return:** -82.96%
- **Ending Balance:** $1,704.48
- **Max Drawdown:** 90.42%
- **Avg Win:** 0.0384%
- **Avg Loss:** -0.0404%
- **Exit Reasons:** {'TP_HIT': 1, 'SL_HIT': 1}

### gbpusd_sweep
- **Pair:** GBPUSD
- **Strategy:** gbpusd_sweep
- **Trades:** 1 (LONG 1, SHORT 0)
- **LONG win rate:** 0.0% (0/1)
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Total Return:** -65.84%
- **Ending Balance:** $3,415.65
- **Max Drawdown:** 65.84%
- **Avg Win:** 0.0000%
- **Avg Loss:** -0.2547%
- **Exit Reasons:** {'SL_HIT': 1}

### gbpusd_continuation
- **Pair:** GBPUSD
- **Strategy:** gbpusd_continuation
- **Trades:** 3 (LONG 1, SHORT 2)
- **LONG win rate:** 100.0% (1/1)
- **SHORT win rate:** 50.0% (1/2)
- **Win Rate:** 66.7%
- **Profit Factor:** 0.98
- **Total Return:** -1.84%
- **Ending Balance:** $9,816.06
- **Max Drawdown:** 45.61%
- **Avg Win:** 0.0000%
- **Avg Loss:** 0.0000%
- **Exit Reasons:** {'TP_HIT': 2, 'SL_HIT': 1}

### xauusd_continuation
- **Pair:** XAUUSD
- **Strategy:** xauusd_continuation
- **Trades:** 2 (LONG 1, SHORT 1)
- **LONG win rate:** 100.0% (1/1)
- **SHORT win rate:** 0.0% (0/1)
- **Win Rate:** 50.0%
- **Profit Factor:** 0.35
- **Total Return:** -262.28%
- **Ending Balance:** $-16,227.51
- **Max Drawdown:** 168.07%
- **Avg Win:** 0.1950%
- **Avg Loss:** 0.0000%
- **Exit Reasons:** {'TP_HIT': 1, 'SL_HIT': 1}

## Basket Combined (One-Position-Per-Symbol)

- **Total Accepted Trades:** 10
- **Rejected (conflicts):** 0
- **Trades per Pair:** {'EURUSD': 4, 'GBPUSD': 4, 'XAUUSD': 2}
- **Trades per Branch:** {'eurusd_orb': 2, 'eurusd_sweep': 1, 'gbpusd_sweep': 1, 'gbpusd_continuation': 3, 'eurusd_continuation': 1, 'xauusd_continuation': 2}
- **Win Rate:** 40.0%
- **Profit Factor:** 0.30
- **Total Return:** -1.84%
- **Ending Balance:** $9,816.06
- **Max Drawdown:** 168.07%

## Risk Summary (Per Branch)

### eurusd_sweep
- balance: -798.7102803727994
- peak_balance: 10000.0
- current_drawdown_pct: 107.98710280372799
- max_drawdown_seen_pct: 107.98710280372799
- consecutive_losses: 1
- halt_reason: MIN_BALANCE_BREACH

### eurusd_continuation
- balance: -6256.499999989201
- peak_balance: 10000.0
- current_drawdown_pct: 162.564999999892
- max_drawdown_seen_pct: 162.564999999892
- consecutive_losses: 1
- halt_reason: MIN_BALANCE_BREACH

### eurusd_orb
- balance: 1704.4796151304636
- peak_balance: 17793.491525425514
- current_drawdown_pct: 90.42076923073307
- max_drawdown_seen_pct: 90.42076923073307
- consecutive_losses: 1
- halt_reason: MAX_DRAWDOWN_BREACH

### gbpusd_sweep
- balance: 3415.6498614957072
- peak_balance: 10000.0
- current_drawdown_pct: 65.84350138504293
- max_drawdown_seen_pct: 65.84350138504293
- consecutive_losses: 1
- halt_reason: MAX_DRAWDOWN_BREACH

### gbpusd_continuation
- balance: 9816.05516574512
- peak_balance: 18046.365573076255
- current_drawdown_pct: 45.606470588239134
- max_drawdown_seen_pct: 45.606470588239134
- consecutive_losses: 1
- halt_reason: MAX_DRAWDOWN_BREACH

### xauusd_continuation
- balance: -16227.512729699964
- peak_balance: 23840.42935483918
- current_drawdown_pct: 168.0671999995087
- max_drawdown_seen_pct: 168.0671999995087
- consecutive_losses: 1
- halt_reason: MIN_BALANCE_BREACH
