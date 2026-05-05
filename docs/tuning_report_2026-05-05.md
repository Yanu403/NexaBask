# Backtest Tuning Report — HFM M5, Jan–May 2026

**Date:** 2026-05-05  
**Data:** HotForex MetaTrader M5, EURUSD/GBPUSD/XAUUSD  
**Entry Model:** Next-bar open + spread (conservative)  
**Same-bar Ambiguity:** SL-first (conservative)  
**Swing Detection:** Backward-only (no look-ahead bias)  
**Position Sizing:** Risk-based with min_risk_distance + max 10 lots cap  

---

## Tuning Summary

Tested 3+ param configurations per strategy × 3 pairs = ~30 backtest runs.

### Key Findings

1. **Sweep strategy (EURUSD):** Best config = `s_r3` (PF=1.00, 30T, WR=36.7%)  
   - Needs: displacement_atr_multiple=0.7, sweep_lookback=60, entry_expiry=24, wider asia range
   - GBPUSD sweep still unprofitable (PF=0.50)

2. **Continuation strategy:** **Not viable on M5 data**  
   - FVG zones only 1-3 pips wide; spread+entry shift immediately breaches SL
   - 26 signals → 0 trades passing risk filter (risk < 3 pips)
   - Even with wider buffer (5 pips), 6 trades → 0% win rate  
   - **Needs M3 or M1 timeframe to work**

3. **ORB strategy (EURUSD):** Best config = `o_r1` (PF=0.63, 10T, WR=30%)  
   - GBPUSD ORB unprofitable (PF=0.25, too many false breakouts)

4. **XAUUSD continuation:** Promising with wide buffer!  
   - stop_buffer=20 pips, min_risk=30 pips → 3T PF=0.99 (nearly breakeven)

---

## Best Configuration Per Branch (Tuned)

| Branch | Strategy | Pair | Config | Trades | WR | PF | Return | DD |
|--------|----------|------|--------|--------|-----|-----|--------|-----|
| eurusd_sweep | SweepFVG | EURUSD | s_r3 | 30 | 36.7% | **1.00** | -0.06% | 5.89% |
| eurusd_orb | ORBRetest | EURUSD | o_r1 | 10 | 30.0% | 0.63 | -1.31% | 2.96% |
| gbpusd_sweep | SweepFVG | GBPUSD | s_r3 | 22 | 22.7% | 0.50 | -4.70% | 4.99% |
| xauusd_cont | Continuation | XAUUSD | xau_c2 | 3 | 33.3% | 0.99 | -0.01% | 0.50% |
| eurusd_cont | ~~Continuation~~ | EURUSD | ❌ SKIP | 0 | — | — | — | — |
| gbpusd_cont | ~~Continuation~~ | GBPUSD | ❌ SKIP | 0 | — | — | — | — |

### Recommended Active Branches (PF > 0.5)
1. **eurusd_sweep (s_r3)** — PF 1.00, 30 trades, near breakeven. Viable foundation.
2. **eurusd_orb (o_r1)** — PF 0.63, diversifies entry style. Complementary to sweep.
3. **xauusd_continuation (xau_c2)** — PF 0.99 on limited data. Monitor with more trades.

### Skip / Disable
- **eurusd_continuation** — Not viable on M5 (FVG too small)
- **gbpusd_continuation** — Same issue
- **gbpusd_sweep** — PF 0.50, not profitable enough

---

## Tuned Parameters

### eurusd_sweep (s_r3)
- max_spread_pips: 4.0 (was 1.5)
- min_sweep_pips: 1.0 (was 3.0)
- min_fvg_pips: 0.3 (was 1.5)
- min_asia_range_pips: 2.0 (was 8.0)
- max_asia_range_pips: 200 (was 80)
- sweep_lookback_bars: 60 (was 12)
- entry_expiry_bars: 24 (was 6)
- displacement_atr_multiple: 0.7 (was 1.4)
- stop_buffer_pips: 2.0 (was 0.5)

### eurusd_orb (o_r1)
- max_spread_pips: 3.0 (was 1.5)
- breakout_buffer_pips: 0.5 (was 1.0)
- retest_tolerance_pips: 1.0 (was 0.5)
- displacement_atr_multiple: 1.0 (was 1.3)
- breakout_lookback_bars: 16 (was 8)
- entry_expiry_bars: 12 (was 8)
- stop_buffer_pips: 1.0 (was 0.5)

### xauusd_continuation (xau_c2)
- pip_size: 0.01
- max_spread_pips: 10.0 (was 1.5)
- min_fvg_pips: 0.03 (was 1.0)
- impulse_lookback_bars: 48 (was 8)
- entry_expiry_bars: 18 (was 8)
- displacement_atr_multiple: 0.8 (was 1.4)
- stop_buffer_pips: 20.0 (was 0.5)
- min_risk_distance_pips: 30.0 (risk manager)

---

## Next Steps

1. **M3 timeframe test** — Strategies (esp. continuation) designed for M3. Test with M3 data.
2. **Forward validation** — Run demo with these tuned params for 2-4 weeks on live MT5.
3. **Trailing stop optimization** — Current trailing ATR multiple may be too tight/loose.
4. **Correlation filter** — EURUSD sweep + ORB may overlap; need conflict resolution.
5. **GBPUSD optimization** — Needs pair-specific tuning (different volatility profile).
