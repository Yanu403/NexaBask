# EURUSD Session Sweep Round 1, 2026-04-22

## Goal

Run the first real sanity pass on the new EURUSD session sweep strategy family using the dropped Jan-Apr 2026 data.

## Data used

Local research artifacts copied into the project:
- `data/eurusd_session_sweep/raw/EURUSDm_M15_202601012200_202604080900.csv`
- `data/eurusd_session_sweep/raw/EURUSDm_M5_202601012205_202604080905.csv`
- `data/eurusd_session_sweep/raw/EURUSDm_M3_202601012203_202604080909.csv`

## Important implementation note

The first blocker was not the setup logic itself, but spread interpretation.
MetaTrader export stored spread in points, not pips. After converting spread to pips, the detector started producing valid M3 candidates.

## Detector funnel after spread fix

### M15
- trade-window rows: 2185
- spread-ok rows: 2168
- Asia-range-ok rows: 2136
- recent sweep rows: 1496
- MSS rows: 27
- FVG rows: 13
- retrace rows: 0
- final signals: 0

### M5
- trade-window rows: 6554
- spread-ok rows: 6503
- Asia-range-ok rows: 6407
- recent sweep rows: 3959
- MSS rows: 45
- FVG rows: 16
- retrace rows: 0
- final signals: 0

### M3
- trade-window rows: 10924
- spread-ok rows: 10838
- Asia-range-ok rows: 10678
- recent sweep rows: 6271
- MSS rows: 93
- FVG rows: 36
- retrace rows: 10
- final signals: 10 before first-touch cleanup
- first-touch sample signals remained and looked structurally plausible

## First-touch cleanup

Initial M3 output repeated the same setup across multiple bars.
This was cleaned up by allowing only the first retrace touch after MSS.
That made the output much closer to discretionary trading intent.

## Round 1 backtest snapshot

### M5
- trades: 0
- verdict: no usable entries yet

### M3
- trades: 3
- win rate: 66.7%
- total return: +1.24%
- profit factor: 2.32
- max drawdown: 1.00%

Trade outcomes:
1. 2026-01-09 LONG, timeout, loss
2. 2026-02-10 LONG, TP hit, win
3. 2026-03-10 SHORT, stop-driven loss in currency terms

## Interpretation

### What looks promising
- The strategy family is not dead on arrival.
- M3 is currently much more aligned with the user's manual execution style than M5.
- The detector can now find a small number of plausible Jan-Apr 2026 setups.

### What is still weak
- Sample size is tiny.
- M5 currently finds no entries.
- Current M15 bias is still only approximated inside the single-timeframe implementation.
- The MSS logic is still simplified.

## Current conclusion

- **Primary research branch for now:** M3 execution
- **Secondary branch:** M5 remains comparison-only until it starts generating valid entries
- The strategy is promising enough to continue, but nowhere near demo/live readiness yet

## Recommended next step

1. refine M3 branch first
2. increase setup count without turning the logic into noise
3. later revisit M5 only if cleaner dual-timeframe bias logic improves it
