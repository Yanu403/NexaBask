# Session Continuation + FVG Strategy Spec

## Status

Research branch only.
This is a companion pattern to the existing session sweep strategy family.

## Intent

Capture days where the market does **not** give a clean liquidity sweep reversal first, but instead prints a valid session displacement and then continues after a retrace.

This branch is meant to complement, not replace, sweep-reversal setups.

## Core idea

Look for:
1. session opens or early-session expansion
2. strong directional displacement
3. a clean FVG / imbalance left by that impulse
4. continuation entry on retrace into the FVG

## Session framing

Initial windows:
- London continuation window: `07:00-11:00 UTC`
- New York continuation window: `12:00-16:00 UTC`

## Long continuation setup

1. During London or NY, a bullish displacement candle appears.
2. Displacement must exceed a minimum ATR-based size.
3. Displacement should break a recent internal swing high or session high.
4. A bullish FVG must be created by the impulse leg.
5. Enter on first retrace into the FVG.
6. Stop goes below the impulse base or below the FVG low with a small buffer.
7. Target uses fixed RR or session-extreme extension.

## Short continuation setup

Mirror of long:
1. bearish displacement
2. break recent internal swing low or session low
3. bearish FVG
4. first retrace entry
5. stop above impulse base
6. fixed RR or session-extreme extension target

## Why this branch exists

The sweep-reversal branch is producing quality, but not enough weekly frequency.
This branch is designed to catch a different day type:
- trend-continuation days
- momentum follow-through after early session imbalance

## Implementation notes

Phase 1 should stay objective:
- ATR-based displacement threshold
- swing break for structure confirmation
- classic 3-candle FVG
- first-touch retrace only
- one position at a time

## Expected relationship to sweep branch

- sweep branch = better for reversal days
- continuation branch = better for momentum days
- combined basket may improve setup count without forcing weaker filters in either branch
