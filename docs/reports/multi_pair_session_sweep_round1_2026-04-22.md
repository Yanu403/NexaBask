# Multi-Pair Session Sweep Round 1, 2026-04-22

## Goal

Check whether expanding the current best EURUSD logic to multiple pairs can move overall setup frequency closer to the target of at least 3 setups per week.

## Shared logic used

All pairs used the same current best branch:
- Asia sweep enabled
- London sweep enabled
- execution timeframe: M3
- `min_sweep_pips=2.0`
- `min_fvg_pips=1.0`
- `entry_expiry_bars=8`

## Pair results

### EURUSD
- trades: 5
- WR: 80.0%
- return: +3.65%
- PF: 4.98
- max DD: 1.00%
- verdict: strong baseline

### GBPUSD
- trades: 5
- WR: 60.0%
- return: -0.21%
- PF: 0.58
- max DD: 1.27%
- verdict: more active, but poor edge with current rule translation

### USDJPY
- trades: 0
- verdict: current logic does not transfer yet

## Combined frequency

### Combined trade count
- total trades: 10
- active weeks: 7
- average trades per active week: 1.43
- max trades in one week: 2

### Weekly distribution
- 2026-W02: 2
- 2026-W04: 1
- 2026-W05: 1
- 2026-W06: 2
- 2026-W07: 2
- 2026-W10: 1
- 2026-W11: 1

## Interpretation

### What worked
- Multi-pair expansion did increase total setup frequency.
- EURUSD remained the strongest and cleanest branch.

### What did not work
- Simply cloning the EURUSD logic is not enough.
- GBPUSD produced more opportunities but with negative expectancy.
- USDJPY produced no trades, meaning the current pip/range/structure assumptions are still mismatched there.

## Strategic conclusion

Multi-pair expansion is directionally correct for frequency, but it should not be treated as a copy-paste solution.
The next smart move is likely:
1. keep EURUSD as the anchor pair
2. adapt GBPUSD separately instead of using the exact same parameters
3. postpone USDJPY unless we want a dedicated JPY-tuned branch

## Review files

Stored locally at:
- `data/multi_pair_session_sweep_round1/summary.json`
- `data/multi_pair_session_sweep_round1/eurusd_summary.json`
- `data/multi_pair_session_sweep_round1/eurusd_ledger.json`
- `data/multi_pair_session_sweep_round1/gbpusd_summary.json`
- `data/multi_pair_session_sweep_round1/gbpusd_ledger.json`
- `data/multi_pair_session_sweep_round1/usdjpy_summary.json`

## Bottom line

- Frequency improved, but not yet to the target of 3 setups per week.
- The best next move is **pair-specific adaptation**, especially for GBPUSD, rather than blindly broadening more symbols with one shared parameter set.
