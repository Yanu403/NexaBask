# Session ORB Round 2, 2026-04-23

## Goal

Improve ORB quality without destroying the frequency advantage that made the branch attractive in round 1.

## Baseline reference

Round 1 baseline:
- trades: 64
- WR: 39.06%
- PF: 1.23
- return: +9.08%
- max DD: 8.72%
- avg trades per active week: 4.27

## Variants tested

### r2_a_stronger_breakout
- `displacement_atr_multiple=1.5`
- `breakout_buffer_pips=1.5`
- `retest_tolerance_pips=0.4`

Result:
- trades: 36
- WR: 36.11%
- PF: 1.06
- return: +1.34%
- max DD: 8.66%
- avg trades per active week: 2.77

Conclusion:
- too harsh
- flow drops sharply without enough quality gain

### r2_b_cleaner_retest
- `breakout_buffer_pips=1.5`
- `retest_tolerance_pips=0.3`
- `entry_expiry_bars=6`
- keep `displacement_atr_multiple=1.3`

Result:
- trades: 44
- WR: 40.91%
- PF: 1.31
- return: +8.04%
- max DD: 9.03%
- avg trades per active week: 3.38

Conclusion:
- best expectancy profile in round 2
- still keeps productivity above the 3-setup target on average
- drawdown is slightly worse than baseline, so this is a quality-up / smoothness-down tradeoff

### r2_c_wider_opening_range
- `opening_range_bars=5`
- `entry_expiry_bars=6`
- keep moderate breakout settings

Result:
- trades: 49
- WR: 36.73%
- PF: 1.17
- return: +4.84%
- max DD: 7.88%
- avg trades per active week: 3.50

Conclusion:
- best drawdown profile in round 2
- but PF and total return are weaker than baseline and weaker than r2_b

## Round 2 interpretation

Round 2 produced a real tradeoff map:
- baseline = strongest raw flow and total return
- r2_b = best PF / cleaner quality mix
- r2_c = best DD control

## Working conclusion

If the priority is:
- **maximum flow** -> keep baseline
- **better expectancy with still-good flow** -> prefer `r2_b_cleaner_retest`
- **lower drawdown** -> prefer `r2_c_wider_opening_range`

The most balanced upgrade candidate is currently `r2_b_cleaner_retest`.
It preserves enough frequency to still solve the original weekly-productivity problem while improving PF meaningfully over baseline.

## Review files

Stored locally at:
- `data/session_orb_round1/eurusd_m3_orb_baseline_summary.json`
- `data/session_orb_round2/eurusd_m3_orb_r2_a_stronger_breakout_summary.json`
- `data/session_orb_round2/eurusd_m3_orb_r2_b_cleaner_retest_summary.json`
- `data/session_orb_round2/eurusd_m3_orb_r2_c_wider_opening_range_summary.json`
