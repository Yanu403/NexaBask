# EURUSD Session Sweep Round 3, 2026-04-22

## Goal

Test whether adding **London session sweep** as an alternative trigger can increase frequency without degrading quality.

## Setup compared

### `r3_asia_only`
- execution timeframe: `M3`
- `min_sweep_pips=2.0`
- `min_fvg_pips=1.0`
- `entry_expiry_bars=8`
- Asia sweep enabled
- London sweep disabled

### `r3_asia_plus_london`
- same parameters as above
- Asia sweep enabled
- London sweep enabled
- London sweep only allowed to trigger entries during the New York window

## Results

| Variant | Trades | WR | Return | PF | Max DD |
|---|---:|---:|---:|---:|---:|
| `r3_asia_only` | 4 | 75.0% | +2.95% | 3.91 | 1.00% |
| `r3_asia_plus_london` | 5 | 80.0% | +3.65% | 4.98 | 1.00% |

## Interpretation

This is the clearest positive refinement so far.

### What improved
- Frequency increased from 4 trades to 5 trades.
- Quality did not degrade.
- In this sample, quality actually improved on both profit factor and total return.

### Why this matters
This strongly supports the user's hypothesis that the real bottleneck is not mostly entry threshold tuning.
The bigger lever is **broadening the trigger universe while keeping the same quality logic after the trigger**.

That means:
- adding London sweep is more promising than over-loosening displacement
- session expansion appears healthier than weakening the core signal structure

## Current best branch

### Best current candidate
`r3_asia_plus_london`

## Data for manual review

Stored locally at:
- `data/eurusd_session_sweep_round3/summary.json`
- `data/eurusd_session_sweep_round3/r3_asia_only_summary.json`
- `data/eurusd_session_sweep_round3/r3_asia_only_ledger.json`
- `data/eurusd_session_sweep_round3/r3_asia_plus_london_summary.json`
- `data/eurusd_session_sweep_round3/r3_asia_plus_london_ledger.json`

## Conclusion

Round 3 confirms a very important direction:
- **session expansion works better than brute-force loosening**
- the next logical step is not weaker filters, but either:
  1. further session-structure expansion, or
  2. multi-pair replication of the same logic
