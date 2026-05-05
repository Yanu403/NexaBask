# EURUSD Session Sweep Research

## Branch purpose

This folder is for the new strategy family based on the user's manual intraday process:
- M15 bias
- M5 or M3 execution
- Asia liquidity sweep
- MSS
- FVG retrace entry

## Why this branch exists

The current XAUUSD H1 and XAUUSD M15 branches are separate workstreams.
This branch is a fresh research path that tries to capture a different edge profile:
more session-driven, more intraday, and likely more aggressive in setup frequency.

## Initial scope

- primary instrument: EURUSD
- first execution branch: M5
- later comparison branch: M3
- session windows: Asia, London, New York

## Immediate next tasks

1. secure clean EURUSD M15 and M5 data with UTC normalization
2. backtest the first objective rule set
3. compare M5 versus M3 execution noise versus trade quality
4. decide whether the M15 bias should stay implicit or be split into a true dual-timeframe engine

## Current implementation state

V1 mechanical logic already exists in:
- `src/xauusd_trading/strategies/eurusd_session_sweep.py`
- `research/experiments/eurusd_session_sweep/inspect_session_sweep.py`

Implemented so far:
- Asia range builder
- sweep detection
- displacement-based MSS approximation
- 3-candle FVG detection
- retrace entry logic

Still missing / still rough:
- proper dual-timeframe M15 bias plus M5 or M3 execution sync
- parameter tuning on actual M5 or M3 EURUSD data
- better MSS definition than the current simplified swing-break model

## Companion branch: continuation pattern

A second pattern branch now exists:
- `src/xauusd_trading/strategies/session_continuation.py`
- `docs/session_continuation_fvg_spec.md`

Purpose:
- complement sweep-reversal setups with continuation-after-displacement setups
- increase basket frequency without weakening the original sweep logic too much

## Important rule

Do not merge this with the H1 or XAUUSD M15 runtime paths.
This branch should stay isolated until it proves its own edge.
