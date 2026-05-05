# Main Basket Session Sweep Round 2, 2026-04-22

## Basket tested

This basket combines the three strongest current branches:
- EURUSD sweep-reversal
- EURUSD continuation
- GBPUSD adapted sweep (`min_sweep_pips=2.5`)

## Component summaries

### EURUSD sweep
- trades: 5
- WR: 80.0%
- PF: 4.98
- return: +3.65%

### EURUSD continuation
- trades: 3
- WR: 100.0%
- return: +3.00%

### GBPUSD adapted sweep
- trades: 5
- WR: 80.0%
- PF: 1.37
- return: +2.66%

## Combined frequency

- total trades: 13
- active weeks: 7
- average trades per active week: 1.86
- max trades in one week: 3

### Weekly distribution
- 2026-W02: 3
- 2026-W04: 1
- 2026-W05: 2
- 2026-W06: 2
- 2026-W07: 2
- 2026-W10: 2
- 2026-W11: 1

## Target comparison

Target:
- at least 3 setups per week

Current basket:
- one week reached the target
- average still below target at 1.86 trades per active week
- target shortfall remains about 1.14 trades per active week

## Interpretation

This is the strongest basket so far.
It proves that the correct direction is a combined approach:
- multiple pairs
- plus multiple session patterns
- plus pair-specific adaptation

### What improved
- This basket is meaningfully more productive than prior baskets.
- It is the first basket to actually hit the weekly target in at least one week.

### What remains unresolved
- The target is not met consistently.
- Productivity is improved, but still not reliable enough to call solved.

## Review file

- `data/main_basket_session_sweep_round2/summary.json`

## Conclusion

Main basket v2 is the best current foundation, but not yet sufficient as the final answer for the productivity goal.
The next likely lever is either:
1. adapt continuation logic to GBPUSD, or
2. tune USDJPY as a third pair-specific branch only if we can make it produce valid setups
