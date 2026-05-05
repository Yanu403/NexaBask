# Session ORB Overlap Review, 2026-04-23

## Goal

Check whether the new EURUSD ORB branch mostly duplicates existing EURUSD session branches or actually adds distinct executable flow.

Compared against existing EURUSD branches:
- EURUSD sweep
- EURUSD continuation

## Ledgers reviewed

- `data/multi_pair_session_sweep_round1/eurusd_ledger.json`
- `data/session_continuation_round1/eurusd_m3_continuation_ledger.json`
- `data/session_orb_round1/eurusd_m3_orb_baseline_ledger.json`

## Raw counts

- ORB trades: 64
- EURUSD sweep trades: 5
- EURUSD continuation trades: 3

## Overlap tests

### 1. Same-day overlap
Definition:
- ORB trade occurs on the same calendar day as an existing EURUSD sweep or continuation trade

Result:
- 7 ORB trades
- 10.94% of ORB trades
- 6 unique dates

### 2. Entry-time proximity
Definition:
- ORB entry within 15 minutes of an existing EURUSD branch entry

Result:
- 4 ORB trades
- 6.25% of ORB trades

Definition:
- ORB entry within 60 minutes of an existing EURUSD branch entry

Result:
- 4 ORB trades
- 6.25% of ORB trades

### 3. Position-time overlap
Definition:
- ORB position lifetime overlaps an already-open EURUSD sweep or continuation position

Result:
- 3 ORB trades
- 4.69% of ORB trades
- all observed overlaps were same-direction, not opposite-direction conflicts

## Example overlaps

- 2026-01-09: ORB LONG 13:33 to 14:45 overlapped EURUSD sweep LONG 13:39 to 14:51
- 2026-01-21: ORB SHORT 15:30 to 15:33 overlapped EURUSD sweep SHORT 15:30 to 16:42
- 2026-02-10: ORB LONG 13:36 to 14:30 overlapped EURUSD sweep LONG 13:39 to 14:15

## Interpretation

This is a strong result for ORB.
The branch does not appear to be mostly double-counting the existing EURUSD session branches.

Key takeaway:
- most ORB trades are on different days or materially different timing
- direct executable conflict rate is low
- overlap that does happen is same-direction, which is operationally easier to manage than opposite-direction conflict

## Current conclusion

- ORB looks like a genuinely additive frequency branch
- raw basket improvement was not just a mirage from duplicated EURUSD signals
- next refinement should focus on quality control, not existential overlap concerns

## Recommended next step

Light ORB refinement aimed at improving PF / DD while preserving most of the new frequency.
