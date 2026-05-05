# XAUUSD Continuation Round 2, 2026-04-23

## Goal

Refine the newly-promoted XAUUSD continuation branch and check whether light parameter loosening can increase frequency without materially harming quality.

## Market / timeframe tested

- pair: XAUUSD
- timeframe: M3

## Baseline reference

Round 1 baseline:
- trades: 3
- WR: 66.7%
- PF: 3.88
- return: +3.00%
- active weeks: 3
- avg trades per active week: 1.0

## Round 2 variants tested

### r2_a_looser_disp
- `displacement_atr_multiple=1.3`
- result: unchanged versus baseline

### r2_b_smaller_fvg
- `min_fvg_pips=6.0`
- result: unchanged versus baseline

### r2_c_longer_expiry
- `entry_expiry_bars=12`
- result: unchanged versus baseline

## Shared result across all tested variants

- trades: 3
- WR: 66.7%
- PF: 3.88
- return: +3.00%
- max DD: 1.00%
- active weeks: 3
- avg trades per active week: 1.0

### Weekly distribution
- 2026-W03: 1
- 2026-W04: 1
- 2026-W07: 1

## Interpretation

The XAUUSD continuation branch is real and clean, but its current bottleneck does not appear to be solved by light threshold loosening.

This is an important result:
- the branch is not fragile
- but it is also not obviously frequency-limited by displacement, FVG size, or entry expiry alone

That suggests the scarcity is more structural, likely tied to the interaction between:
- impulse detection
- structure break requirement
- first retrace rule
- trade window definition

## Current conclusion

- Keep XAUUSD continuation in the basket as a valid branch
- Do not expect easy extra frequency from small threshold tweaks
- If more XAUUSD frequency is needed, the next refinement should target structure logic or session definition, not just smaller numeric filters

## Review files

Stored locally at:
- `data/xauusd_continuation_round1/xauusd_m3_continuation_baseline_summary.json`
- `data/xauusd_continuation_round2/xau_cont_r2_a_looser_disp_summary.json`
- `data/xauusd_continuation_round2/xau_cont_r2_b_smaller_fvg_summary.json`
- `data/xauusd_continuation_round2/xau_cont_r2_c_longer_expiry_summary.json`
