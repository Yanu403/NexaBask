# GBPUSD Session Sweep Round 1, 2026-04-22

## Goal

Adapt GBPUSD away from the EURUSD copy-paste parameter set and see whether pair-specific tuning can preserve frequency while restoring edge.

## Baseline from multi-pair copy

### `gbp_base_copy`
- trades: 5
- WR: 60.0%
- return: -0.21%
- PF: 0.58
- max DD: 1.27%

This confirmed GBPUSD was active enough, but the copied EURUSD parameters did not fit the pair well.

## Adaptation tests

### `gbp_a_stricter_sweep`
- `min_sweep_pips=2.5`
- trades: 5
- WR: 80.0%
- return: +2.66%
- PF: 1.37
- max DD: 1.00%

### `gbp_d_combo_tighter`
- `min_sweep_pips=2.5`
- `min_fvg_pips=1.5`
- `displacement_atr_multiple=1.6`
- trades: 2
- WR: 100.0%
- return: +3.73%
- max DD: 0.00%

## Interpretation

### Key finding
Pair-specific adaptation works.
Just increasing GBPUSD sweep strictness from 2.0 to 2.5 was enough to turn the branch from slightly negative to clearly positive, without losing trade count.

### Trade-off
- `gbp_a_stricter_sweep` is the more practical branch, because it keeps 5 trades.
- `gbp_d_combo_tighter` is cleaner on paper, but too sparse to help the weekly productivity target much.

## Current best GBPUSD branch

### Best practical candidate
`gbp_a_stricter_sweep`

Why:
- preserves activity
- restores positive expectancy
- keeps drawdown low

## Strategic impact

This is strong evidence that multi-pair expansion should continue as **pair-specific adaptation**, not as a copy-paste rollout.

## Review files

Stored locally at:
- `data/gbpusd_session_sweep_round1/gbp_a_stricter_sweep_summary.json`
- `data/gbpusd_session_sweep_round1/gbp_a_stricter_sweep_ledger.json`
- `data/gbpusd_session_sweep_round1/gbp_d_combo_tighter_summary.json`
- `data/gbpusd_session_sweep_round1/gbp_d_combo_tighter_ledger.json`

## Conclusion

GBPUSD is now a valid second candidate branch, but even after adaptation the combined weekly frequency target is still not clearly solved yet.
That means the next step is likely:
1. combine EURUSD + adapted GBPUSD as the main basket
2. then decide whether to adapt USDJPY or expand session logic further
