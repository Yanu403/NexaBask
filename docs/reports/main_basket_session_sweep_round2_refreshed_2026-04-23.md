# Main Basket Session Sweep Round 2 Refreshed, 2026-04-23

## Why this refresh was needed

A backtest metric bug was fixed:
- small profitable trades could previously show negative `pnl_pct`
- continuation branch summaries therefore needed to be refreshed

## Refreshed basket

- EURUSD sweep
- EURUSD continuation
- GBPUSD adapted sweep
- GBPUSD continuation

## Refreshed component summaries

### EURUSD sweep
- trades: 5
- WR: 80.0%
- PF: 4.98
- return: +3.65%

### EURUSD continuation
- trades: 3
- WR: 66.7%
- PF: 3.94
- return: +3.00%

### GBPUSD adapted sweep
- trades: 5
- WR: 80.0%
- PF: 1.37
- return: +2.66%

### GBPUSD continuation
- trades: 1
- WR: 100.0%
- return: +2.00%
- still too sparse to matter much yet

## Combined frequency

- total trades: 14
- active weeks: 7
- average trades per active week: 2.00
- max trades in one week: 3

### Weekly distribution
- 2026-W02: 3
- 2026-W04: 1
- 2026-W05: 2
- 2026-W06: 2
- 2026-W07: 2
- 2026-W10: 3
- 2026-W11: 1

## Target comparison

Target:
- at least 3 setups per week

Refreshed result:
- target hit in 2 weeks
- average still below target at 2.00 trades per active week
- shortfall still about 1.00 trade per active week

## Interpretation

This refresh improves confidence in the basket and confirms that:
- the combined direction is correct
- the basket is stronger than earlier summaries implied
- but productivity is still not consistently solved

## Bottom line

The current basket is now better described as:
- viable
- increasingly productive
- still short of the desired weekly consistency

## Review file

- `data/main_basket_session_sweep_round2_refreshed/summary.json`
