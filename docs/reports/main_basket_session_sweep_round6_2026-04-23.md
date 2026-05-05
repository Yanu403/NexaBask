# Main Basket Session Sweep Round 6, 2026-04-23

## Goal

Rebuild the basket using the refined ORB candidate `r2_b_cleaner_retest` instead of the noisier raw ORB baseline.

## Basket composition

- EURUSD sweep
- EURUSD continuation
- GBPUSD adapted sweep
- GBPUSD continuation
- XAUUSD continuation
- EURUSD ORB (`r2_b_cleaner_retest`)

## Component snapshot

### EURUSD sweep
- trades: 5
- PF: 4.98
- return: +3.65%
- max DD: 1.00%

### EURUSD continuation
- trades: 3
- PF: 3.94
- return: +3.00%
- max DD: 1.00%

### GBPUSD adapted sweep
- trades: 5
- PF: 1.37
- return: +2.66%
- max DD: 1.00%

### GBPUSD continuation
- trades: 1
- return: +2.00%
- max DD: 0.00%

### XAUUSD continuation
- trades: 3
- PF: 3.88
- return: +3.00%
- max DD: 1.00%

### EURUSD ORB r2_b
- trades: 44
- PF: 1.31
- return: +8.04%
- max DD: 9.03%
- avg trades per active week: 3.38

## Combined productivity

- total trades: 61
- active weeks: 13
- avg trades per active week: 4.69
- max trades in one week: 7
- weeks hitting target (>= 3 trades): 13 of 13

### Weekly distribution
- 2026-W02: 5
- 2026-W03: 5
- 2026-W04: 4
- 2026-W05: 4
- 2026-W06: 7
- 2026-W07: 6
- 2026-W08: 3
- 2026-W09: 3
- 2026-W10: 4
- 2026-W11: 4
- 2026-W12: 6
- 2026-W13: 6
- 2026-W14: 4

## Interpretation

This is a strong basket result.
The refined ORB branch keeps the basket well above the target of 3 setups per active week while improving ORB quality relative to the raw baseline.

Compared with the earlier raw ORB basket view:
- frequency is lower than the raw ORB baseline version
- but quality is better balanced
- the basket still clears the user productivity target comfortably

## Current conclusion

The basket now appears to have crossed an important threshold:
- productivity target is solved on a raw, overlap-aware-reviewed basis
- ORB is now a central branch, not an optional extra
- the next step should shift from “find more setups” to “portfolio hygiene and execution realism”

## Review file

- `data/main_basket_session_sweep_round6/summary.json`
