# EURUSD Session Sweep Round 2, 2026-04-22

## Goal

Increase M3 setup frequency without immediately collapsing quality.

## Test focus

Round 2 tested only light-to-moderate relaxations first.
This was intentional, because the round 1 branch was too tight, but the wrong kind of looseness could quickly turn into noise.

## Variants tested

### `base_v1`
- trades: 3
- WR: 66.7%
- return: +1.24%
- PF: 2.32
- max DD: 1.00%

### `r2_a_looser_sweep`
- params:
  - `min_sweep_pips=2.0`
  - `min_fvg_pips=1.0`
  - `entry_expiry_bars=8`
- trades: 4
- WR: 75.0%
- return: +2.95%
- PF: 3.91
- max DD: 1.00%

### `r2_b_looser_disp`
- params:
  - `min_sweep_pips=2.0`
  - `displacement_atr_multiple=1.1`
  - `min_fvg_pips=1.0`
  - `entry_expiry_bars=8`
- trades: 8
- WR: 50.0%
- return: -1.11%
- PF: 1.00
- max DD: 3.94%

## Interpretation

### What improved
- Light relaxation worked.
- `r2_a_looser_sweep` increased setup count slightly while improving headline performance.

### What broke
- Relaxing displacement too far (`r2_b_looser_disp`) doubled trade count, but degraded quality sharply.
- This is a classic sign that more frequency is possible, but the displacement filter still matters a lot.

## Current best round 2 direction

### Best candidate so far
`r2_a_looser_sweep`

Why:
- more trades than base
- still clean drawdown
- quality did not collapse

## Backtest data for manual review

Stored locally at:
- `data/eurusd_session_sweep_round2/base_v1_summary.json`
- `data/eurusd_session_sweep_round2/base_v1_ledger.json`
- `data/eurusd_session_sweep_round2/r2_a_looser_sweep_summary.json`
- `data/eurusd_session_sweep_round2/r2_a_looser_sweep_ledger.json`
- `data/eurusd_session_sweep_round2/r2_b_looser_disp_summary.json`
- `data/eurusd_session_sweep_round2/r2_b_looser_disp_ledger.json`
- `data/eurusd_session_sweep_round2/summary.json`

## Conclusion

The branch is still too sparse overall, but we now have evidence that:
- setup count can be increased a bit
- loosen too much on displacement and quality degrades fast
- M3 remains the only execution branch currently worth refining

## Recommended next step

Continue with targeted M3 refinement around:
1. sweep threshold
2. FVG minimum size
3. entry expiry

Do **not** relax displacement too aggressively again unless paired with a stronger M15 bias filter.
