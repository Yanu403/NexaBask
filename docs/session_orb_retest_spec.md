# Session Opening-Range Breakout Retest Spec

## Status

Research branch only.
This branch is a third session-pattern family beside:
- sweep-reversal
- continuation-after-displacement

## Intent

Capture session expansion days that do not begin with a clean liquidity sweep and do not necessarily retrace into a classic continuation FVG early enough.

## Core idea

1. define a small opening range at the start of the session
2. require a strong breakout beyond that range
3. do not chase the breakout candle itself
4. wait for the first retest of the broken range boundary
5. enter in breakout direction with fixed RR

## Session framing

Initial windows:
- London: 07:00-11:00 UTC
- New York: 12:00-16:00 UTC

## Opening range

Initial phase-1 default:
- first `opening_range_bars` of each active session
- store:
  - opening range high
  - opening range low
  - opening range size

## Long setup

1. session opening range is formed
2. bullish displacement candle closes above opening-range high by at least a small breakout buffer
3. breakout must satisfy ATR-based displacement threshold
4. wait for first retest of the broken opening-range high
5. enter long on retest
6. stop below breakout impulse low with small buffer
7. target at fixed RR

## Short setup

Mirror of long:
1. bearish displacement below opening-range low
2. first retest of broken range low
3. stop above breakout impulse high
4. fixed RR target

## Why this branch exists

The basket needed a higher-frequency pattern branch that still stays objective and session-driven.
This branch is meant to capture clean session expansion days rather than reversal or continuation-with-FVG days.

## Important caution

Backtest frequency from this branch should first be treated as raw opportunity flow, not immediately as executable portfolio flow, because it may overlap with other EURUSD branches in the same week or same session.
