# Main Basket Session Sweep Round 6 Priority Review, 2026-04-23

## Goal

Define practical branch priority / conflict rules for the current basket so execution can be deterministic when multiple branch signals compete.

## Basket branches reviewed

- EURUSD sweep
- EURUSD continuation
- GBPUSD adapted sweep
- GBPUSD continuation
- XAUUSD continuation
- EURUSD ORB r2_b

## Actual conflict map observed

Total overlapping conflict pairs found in the current basket ledgers:
- 3

Conflict pair breakdown:
- `eurusd_sweep` vs `gbpusd_sweep`: 2
- `eurusd_orb` vs `eurusd_sweep`: 1

Branch conflict counts:
- EURUSD sweep: 3
- GBPUSD sweep: 2
- EURUSD ORB: 1
- all other branches: 0

## Branch scorecard snapshot

### EURUSD sweep
- PF: 4.98
- WR: 80.0%
- DD: 1.00%
- conflicts observed: 3

### EURUSD continuation
- PF: 3.94
- WR: 66.7%
- DD: 1.00%
- conflicts observed: 0

### XAUUSD continuation
- PF: 3.88
- WR: 66.7%
- DD: 1.00%
- conflicts observed: 0

### GBPUSD adapted sweep
- PF: 1.37
n- WR: 80.0%
- DD: 1.00%
- conflicts observed: 2

### EURUSD ORB r2_b
- PF: 1.31
- WR: 40.9%
- DD: 9.03%
- conflicts observed: 1

### GBPUSD continuation
- tiny sample, keep lowest confidence priority for now

## Suggested branch priority order

1. EURUSD sweep
2. EURUSD continuation
3. XAUUSD continuation
4. GBPUSD adapted sweep
5. EURUSD ORB r2_b
6. GBPUSD continuation

## Why this order

Principles used:
- higher PF first
- lower DD first
- cleaner branch first when conflict frequency is small
- ORB remains essential for productivity, but when a direct conflict appears, the cleaner higher-PF branches should win
- tiny-sample branches stay low confidence until they have more evidence

## Simple conflict rules recommendation

### Rule 1: one position per symbol
- only one live trade per symbol at a time

### Rule 2: if two branches on the same symbol compete, use priority order
For EURUSD this means:
- sweep beats continuation
- continuation beats ORB
- sweep beats ORB

### Rule 3: if symbols differ, overlapping positions are allowed
This keeps productivity high and matches the realism review results.

### Rule 4: keep ORB as the default flow engine, not the default conflict winner
ORB solves frequency, but it should not automatically overrule cleaner branches.

## Priority model result

Under the one-position-per-symbol model with the suggested priority ordering:
- accepted trades: 60
- rejected trades: 1
- active weeks: 13
- avg trades per active week: 4.62
- weeks hitting target: 13 / 13

Observed rejection example:
- EURUSD ORB on 2026-01-21 15:30 was rejected when applying same-symbol conflict handling

## Current conclusion

The basket does not need complex conflict orchestration yet.
A simple rule set is enough:
- one position per symbol
- branch priority for same-symbol conflicts
- allow cross-symbol overlap

This preserves nearly all of the basket's flow while making execution deterministic and cleaner.

## Review file

- `data/main_basket_session_sweep_round6_priority/summary.json`
