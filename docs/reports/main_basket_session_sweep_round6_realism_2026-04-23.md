# Main Basket Session Sweep Round 6 Realism Review, 2026-04-23

## Goal

Move from raw research-basket counting to a simple executable portfolio realism check.

## Basket reviewed

- EURUSD sweep
- EURUSD continuation
- GBPUSD adapted sweep
- GBPUSD continuation
- XAUUSD continuation
- EURUSD ORB `r2_b_cleaner_retest`

Raw basket reference:
- total trades: 61
- active weeks: 13
- avg trades per active week: 4.69
- weeks hitting target: 13 / 13

## Realism models tested

### Model A: global one-position rule
Assumption:
- only one position may be open across the entire portfolio at any time

Result:
- accepted trades: 58
- rejected trades: 3
- accept rate: 95.08%
- active weeks: 13
- avg trades per active week: 4.46
- max trades in one week: 7
- weeks hitting target: 13 / 13

Branch counts kept:
- EURUSD ORB: 43
- EURUSD sweep: 4
- EURUSD continuation: 3
- GBPUSD sweep: 4
- GBPUSD continuation: 1
- XAUUSD continuation: 3

### Model B: one position per symbol
Assumption:
- one open position per symbol
- different symbols may overlap

Result:
- accepted trades: 60
- rejected trades: 1
- accept rate: 98.36%
- active weeks: 13
- avg trades per active week: 4.62
- max trades in one week: 7
- weeks hitting target: 13 / 13

Branch counts kept:
- EURUSD ORB: 43
- EURUSD sweep: 5
- EURUSD continuation: 3
- GBPUSD sweep: 5
- GBPUSD continuation: 1
- XAUUSD continuation: 3

## Conflict examples

### Global one-position conflicts observed
- GBPUSD sweep on 2026-01-09 13:51 rejected due to overlapping open position
- EURUSD ORB on 2026-01-21 15:30 rejected due to overlapping open position
- EURUSD sweep on 2026-02-10 13:39 rejected due to overlapping open position

### Per-symbol conflict observed
- EURUSD ORB on 2026-01-21 15:30 rejected due to overlap with another EURUSD branch

## Interpretation

This is a strong realism result.
The raw basket does not collapse when simple executable constraints are imposed.

Key finding:
- the basket is not overdependent on impossible simultaneous trades
- even a harsh global one-position rule still leaves the basket comfortably above the user's target

## Current conclusion

The project has likely crossed from "interesting research basket" into "tradable portfolio candidate" territory.
The next work should focus on:
- branch priority rules
- portfolio-level risk sizing
- execution ordering and conflict handling
- then paper-trade style portfolio simulation if needed

## Review file

- `data/main_basket_session_sweep_round6_realism/summary.json`
