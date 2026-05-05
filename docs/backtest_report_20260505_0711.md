# Session Basket Backtest Report
**Date:** 2026-05-05 07:11
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
- **Total Return:** -23.11%
- **Ending Balance:** $7,689.08
- **Max Drawdown:** 23.11%
- **Avg Win:** 0.0000%
- **Avg Loss:** -0.1583%
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
- **SHORT win rate:** 57.1% (4/7)
- **Win Rate:** 50.0%
- **Profit Factor:** 0.94
- **Total Return:** -2.33%
- **Ending Balance:** $9,766.85
- **Max Drawdown:** 24.16%
- **Avg Win:** 0.0490%
- **Avg Loss:** -0.0454%
- **Exit Reasons:** {'TP_HIT': 3, 'SL_HIT': 4, 'TIMEOUT': 1}

### gbpusd_sweep
- **Pair:** GBPUSD
- **Strategy:** gbpusd_sweep
- **Trades:** 1 (LONG 1, SHORT 0)
- **LONG win rate:** 0.0% (0/1)
- **Win Rate:** 0.0%
- **Profit Factor:** 0.00
- **Total Return:** -39.62%
- **Ending Balance:** $6,038.42
- **Max Drawdown:** 39.62%
- **Avg Win:** 0.0000%
- **Avg Loss:** -0.2547%
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

- **Total Accepted Trades:** 12
- **Rejected (conflicts):** 0
- **Trades per Pair:** {'EURUSD': 9, 'GBPUSD': 1, 'XAUUSD': 2}
- **Trades per Branch:** {'eurusd_orb': 8, 'eurusd_sweep': 1, 'gbpusd_sweep': 1, 'xauusd_continuation': 2}
- **Win Rate:** 41.7%
- **Profit Factor:** 0.35
- **Total Return:** -262.28%
- **Ending Balance:** $-16,227.51
- **Max Drawdown:** 168.07%

## Risk Summary (Per Branch)

### eurusd_sweep
- balance: 7689.076000000188
- peak_balance: 10000.0
- current_drawdown_pct: 23.109239999998117
- max_drawdown_seen_pct: 23.109239999998117
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
- balance: 9766.852000000494
- peak_balance: 12878.09600000066
- current_drawdown_pct: 24.159192476900365
- max_drawdown_seen_pct: 24.159192476900365
- consecutive_losses: 3
- halt_reason: MAX_DRAWDOWN_BREACH

### gbpusd_sweep
- balance: 6038.416000000037
- peak_balance: 10000.0
- current_drawdown_pct: 39.615839999999636
- max_drawdown_seen_pct: 39.615839999999636
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
- balance: -16227.512729699964
- peak_balance: 23840.42935483918
- current_drawdown_pct: 168.0671999995087
- max_drawdown_seen_pct: 168.0671999995087
- consecutive_losses: 1
- halt_reason: MIN_BALANCE_BREACH
