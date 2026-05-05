# EURUSD Session Sweep + MSS + FVG Strategy Spec

## Status

Research branch only.
This is a **new strategy family**, separate from the current XAUUSD H1 and XAUUSD M15 branches.

## Intent

Translate the user's manual intraday workflow into a bot-friendly rule set:
- bias from M15
- execution from M5 or M3
- focus on London and New York sessions
- look for Asia session liquidity sweep
- require displacement / momentum and MSS
- enter on FVG or imbalance retrace

## Target market

- Primary: `EURUSD`
- Bias timeframe: `M15`
- Execution timeframe: `M5` first, `M3` optional follow-up branch

## Core idea

The bot should not chase every breakout.
It should wait for:
1. a clear Asia range
2. a liquidity sweep beyond that range
3. a post-sweep shift in structure
4. displacement strong enough to leave an imbalance / FVG
5. a retrace into that FVG during the active session window

## Session model

### Asia session range
Initial default, subject to later tuning:
- Asia range collection: `00:00-06:00 UTC`
- Stored values:
  - `asia_high`
  - `asia_low`
  - `asia_mid`
  - `asia_range_size`

### Trade windows
Initial default, subject to later tuning:
- London window: `07:00-11:00 UTC`
- New York window: `12:00-16:00 UTC`
- No new trade outside those windows

## High-level setup logic

### Long setup
1. Build the Asia range from the M15 context.
2. During London or NY, price sweeps below `asia_low`.
3. Sweep must exceed a minimum excursion threshold.
4. After the sweep, market prints bullish displacement.
5. That displacement must cause bullish MSS.
6. Detect a bullish FVG left by the displacement leg.
7. Enter on retrace into the FVG.
8. Stop loss goes below sweep low.
9. Take profit targets opposing liquidity, initially `asia_high` or a minimum fixed RR.

### Short setup
Mirror of long:
1. Sweep above `asia_high`.
2. Bearish displacement.
3. Bearish MSS.
4. Bearish FVG.
5. Entry on retrace.
6. Stop loss above sweep high.
7. Take profit toward `asia_low` or fixed RR.

## Rule translation details

### 1. M15 bias
M15 is not for late entry timing, but for context.
Initial bias rules to test:
- bias long if the sweep is below Asia low and the post-sweep M15 displacement closes back above the range edge or above an internal pivot
- bias short if the sweep is above Asia high and the post-sweep M15 displacement closes back below the range edge or below an internal pivot
- optional trend filter later, not required in phase 1

### 2. Sweep definition
A valid sweep should be objective.
Initial version:
- wick extends beyond Asia range boundary by at least `min_sweep_pips`
- close should return inside or near the range boundary within the same or next execution candle
- only first meaningful sweep per side per session is eligible

Candidate parameter:
- `min_sweep_pips = 2.0 to 5.0` on EURUSD

### 3. Displacement / momentum
Initial mechanical definition:
- displacement candle body >= `body_atr_multiple * ATR(exec_tf)`
- candle closes in the direction opposite the sweep
- candle breaks at least one recent micro swing

Candidate parameter:
- `body_atr_multiple = 1.2 to 1.8`

### 4. MSS (market structure shift)
Initial rule:
- for longs, after sweep low, price must close above the latest execution swing high
- for shorts, after sweep high, price must close below the latest execution swing low
- MSS must occur inside the allowed London/NY window

### 5. FVG / imbalance
Use the classic 3-candle definition.

#### Bullish FVG
For candles `A, B, C`:
- `low(C) > high(A)`
- FVG zone = `[high(A), low(C)]`

#### Bearish FVG
- `high(C) < low(A)`
- FVG zone = `[high(C), low(A)]`

Additional filters:
- minimum FVG size in pips
- only accept the FVG created by the displacement leg that also caused MSS

### 6. Entry logic
Initial priority:
- wait for first retrace into FVG after MSS
- entry mode candidates:
  - touch of FVG boundary
  - 50% FVG fill
- if no retrace within `entry_expiry_bars`, invalidate setup

### 7. Stop loss logic
Initial version:
- long SL below sweep low minus small buffer
- short SL above sweep high plus small buffer

### 8. Target logic
Initial backtest version should support two target styles:
- fixed RR, e.g. 2R or 3R
- opposing liquidity target, e.g. Asia opposite boundary

### 9. Session hygiene / trade management
Initial restrictions:
- max one trade per direction per session window
- max one live position at a time
- skip if spread exceeds threshold
- invalidate setup after session cutoff

## Phase 1 bot version

To keep the first build objective and testable, phase 1 should deliberately exclude:
- discretionary higher-timeframe narrative
- news filters
- correlated DXY confirmation
- multiple nested FVG choices
- advanced liquidity pools outside Asia range

## Data requirements

To backtest this properly we need:
- EURUSD M15 OHLCV for bias/session construction
- EURUSD M5 OHLCV for execution, or M3 for the later branch
- consistent UTC normalization
- spread column or approximation where possible

## Implementation plan

### Phase A
- write exact parameter schema
- implement session/range builder
- implement sweep detector
- implement MSS detector
- implement FVG detector

### Phase A status now
V1 mechanical implementation now exists in `src/xauusd_trading/strategies/eurusd_session_sweep.py`.
Current version already includes:
- Asia range builder
- sweep detection
- displacement-based MSS approximation
- classic 3-candle FVG detection
- retrace entry into the detected FVG zone

Current limitations:
- still assumes a single execution-timeframe dataset
- M15 bias is represented structurally, not yet through a separate synchronized M15 feed
- MSS is still a simplified swing-break model, not a multi-layer structure engine

### Phase B
- build M15 bias + M5 execution prototype
- run first sanity backtests
- measure trade frequency by session

### Phase C
- compare M5 versus M3 execution branch
- decide whether M3 adds edge or only adds noise

## Honest risk note

This strategy family can be made algorithmic, but only if the definitions stay strict.
If the spec slips back into subjective chart-reading language, the bot will become fragile or fake-precise.

That means the right path is:
- objective rule first
- aggressive tuning later
- no hindsight storytelling
