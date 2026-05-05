# Main Basket Session Sweep Round 1, 2026-04-22

## Basket tested

The current best practical basket combines:
- EURUSD, current best Asia+London M3 branch
- GBPUSD, adapted branch with stricter sweep (`min_sweep_pips=2.5`)

## Pair summaries

### EURUSD
- trades: 5
- WR: 80.0%
- PF: 4.98
- return: +3.65%

### GBPUSD
- trades: 5
- WR: 80.0%
- PF: 1.37
- return: +2.66%

## Combined weekly frequency

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

## Target comparison

Target:
- at least 3 setups per week

Current basket:
- average 1.43 trades per active week
- shortfall versus target: about 1.57 trades per active week

## Interpretation

This basket is clearly healthier than single-pair EURUSD alone.
However, it still does not reach the desired productivity target.

### What this means
- pair-specific adaptation works
- EURUSD + adapted GBPUSD is a valid foundation
- but the basket still needs one more productive source of setups

## Practical next move

The most likely next lever is:
1. adapt a third pair only if it can be tuned properly, or
2. add another valid session pattern branch, not just more aggressive filtering

## Review file

- `data/main_basket_session_sweep_round1/summary.json`

## Bottom line

The basket is good enough to continue building on, but not yet productive enough for the weekly target.
