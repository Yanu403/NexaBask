# Session ORB Round 1, 2026-04-23

## Goal

Test a third session-pattern family, opening-range breakout retest (ORB), to see whether it can solve the basket's setup-frequency problem more effectively than forcing weaker tweaks into the existing sweep and continuation branches.

## Market / timeframe tested

- pair: EURUSD
- timeframe: M3

## Baseline parameters

- `opening_range_bars=4`
- `displacement_atr_multiple=1.3`
- `breakout_buffer_pips=1.0`
- `retest_tolerance_pips=0.5`
- `breakout_lookback_bars=8`
- `entry_expiry_bars=8`
- `rr_target=2.0`

## Round 1 result

- trades: 64
- WR: 39.06%
- PF: 1.23
- return: +9.08%
- max DD: 8.72%
- active weeks: 15
- avg trades per active week: 4.27

### Weekly distribution
- 2026-W01: 1
- 2026-W02: 4
- 2026-W03: 5
- 2026-W04: 2
- 2026-W05: 2
- 2026-W06: 6
- 2026-W07: 6
- 2026-W08: 5
- 2026-W09: 4
- 2026-W10: 5
- 2026-W11: 4
- 2026-W12: 6
- 2026-W13: 7
- 2026-W14: 6
- 2026-W15: 1

## Interpretation

This is the first branch that meaningfully solves the setup-frequency problem.
It is materially more productive than the sweep and continuation branches.

What is good:
- objective and lightweight logic
- positive expectancy profile in the first run
- enough flow to actually matter at the basket level

What needs caution:
- quality is lower than the cleaner low-frequency branches
- drawdown is higher than the tiny-sample continuation branches
- raw basket counts may overstate executable portfolio flow because EURUSD branches can overlap in the same session or week

## Basket impact (raw frequency view)

When added to the current basket, raw combined frequency rises to:
- total trades: 81
- active weeks: 15
- avg trades per active week: 5.40
- weeks hitting target (>=3 trades): 13

This strongly suggests the missing ingredient was a breakout-expansion pattern, not more threshold loosening in existing branches.

## Current conclusion

- Keep ORB as a real branch candidate
- Do not treat raw combined counts as final executable portfolio statistics yet
- Next logical step is overlap-aware basket review or light ORB refinement to reduce noise without killing flow

## Review files

Stored locally at:
- `data/session_orb_round1/eurusd_m3_orb_baseline_summary.json`
- `data/session_orb_round1/eurusd_m3_orb_baseline_ledger.json`
- `data/main_basket_session_sweep_round5/summary.json`
