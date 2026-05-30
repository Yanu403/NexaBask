# Architecture, realistic version

## 1. What the bot should look like, realistically

The diagram you sent is good as an aspiration, but for the current state of the project, the realistic version is this:

```text
Market Data
   |
   v
Data Validation / Normalization
   |
   v
Feature Pipeline
   |
   v
Strategy Engine
   |
   v
Risk Engine
   |
   v
Execution Adapter
   |
   v
Trade Log / Metrics / Feedback
```

## 2. Why this version is better for us now

Because currently we have no strong reason to centralize the system around:
- a full ML layer
- a core LLM layer

What has already proven important is:
- valid data
- consistent features
- fair backtesting
- fair walk-forward
- strict risk control
- safe execution

## 3. Target module responsibilities

### Data layer
Responsibilities:
- load CSV / broker feed
- standardize schema
- validate timestamp, duplicates, gaps, spread sanity
- isolate symbol and timeframe specific quirks

Should not contain:
- signal logic
- risk logic
- order placement

### Feature pipeline
Responsibilities:
- EMA, ATR, RSI, spread features
- candle structure
- volatility and session features
- optional regime labels

Should not contain:
- SL/TP rules
- broker logic

### Strategy engine
Responsibilities:
- consume clean features
- output setup / signal candidate
- no broker side effects
- no direct file IO if possible

Minimal output:
- side
- entry condition
- stop reference
- target reference
- reason tags

### Risk engine
Responsibilities:
- position sizing
- max concurrent exposure
- spread filter
- drawdown monitor
- daily loss guard
- kill switch

This must be a hard gate before execution.

### Execution adapter
Responsibilities:
- paper trade or broker order submit
- idempotent order actions
- retry rules
- fill/update/cancel handling
- persistent state and journal for runtime decisions

### Feedback / reporting
Responsibilities:
- trade ledger
- equity curve
- per-strategy metrics
- out-of-sample reports
- error logs and execution events

## 4. Implemented foundation, after cleanup

The initial reusable foundation is now in place:
- `data/loader.py` for basic OHLCV data loading + validation
- `features/indicators.py` for EMA, ATR, RSI, session features
- `strategies/base.py` for the strategy interface
- `strategies/tf001.py` for proof-of-concept strategy implementation
- `strategies/sr_sd_v35.py` for second research candidate migration
- `strategies/sr_sd_v35_short.py` for refined short mirror
- `strategies/sr_ema_v41.py` for bias-prone static S/R + EMA comparison
- `backtesting/engine.py` for minimal unified backtest engine
- `risk/manager.py` for sizing + drawdown / loss guards
- `execution/paper.py` for paper-trade state/journal flow
- `execution/portfolio.py` for candidate portfolio signal collection
- `data/mt5.py` for MT5 data bridge from terminal to strategy engine
- `reporting/metrics.py` for summary metrics
- `reporting/ledger.py` for trade ledger export
- `run_backtest.py` as single entry point for backtesting
- `run_paper_trade.py` for CSV-based candidate portfolio paper-trade runner
- `run_paper_trade_mt5.py` for MT5-connected paper-trade runner
- `run_paper_trade_mt5_loop.py` for MT5-connected periodic runtime

This means the project is no longer just a pile of experimental scripts. It now has a reusable core.

## 5. Where ML and LLM fit later

### ML, only if proven useful
ML comes in after the baseline strategy engine is clean.
Realistic roles:
- regime classifier
- probability calibration
- trade quality scoring
- feature importance study

Not a total replacement of all logic from scratch.

### LLM, not core alpha
LLM is suitable later for:
- operator summary
- anomaly explanation
- strategy comparison notes
- natural language reporting
- maybe regime commentary

LLM must not be the primary source of entry/exit without a very strict validation framework.

## 6. Suggested evolution path

### Stage 1, now
**Research-first layered**

- research scripts still exist
- common logic is being extracted
- no fake abstraction

### Stage 2, when repeated logic appears
**Modular layered core**

Add reusable modules for:
- loaders
- features
- signals
- backtest
- metrics

### Stage 3, before live trading
**Operational architecture**

Add:
- a richer risk service/module than the current basic guards
- execution adapter
- persistent trade log connected to paper/live flow
- alerting and kill switch

### Stage 4, only if justified
**ML-assisted architecture**

Add ML scoring/regime layer on top of the feature pipeline, not directly on top of the broker.

## 7. Current project mapping

### Current research assets
- `research/experiments/tf001/` → early EMA pullback family
- `research/experiments/sr_sd/` → S/R plus supply-demand experiments
- `research/experiments/sr_ema/` → S/R plus EMA family, includes biased result history
- `research/walkforward/` → fairness check and no-look-ahead validation
- `research/cross_asset/` → transferability sanity check

### Current target core
- `src/xauusd_trading/data/`
- `src/xauusd_trading/features/`
- `src/xauusd_trading/strategies/`
- `src/xauusd_trading/risk/`
- `src/xauusd_trading/execution/`
- `src/xauusd_trading/reporting/`
- `src/xauusd_trading/backtesting/`
- `src/xauusd_trading/models/`

## 8. Non-negotiable rules for this project

1. Strategy first, glamour later
2. No look-ahead, ever
3. Research and production paths must be separated
4. Risk layer is mandatory, not optional
5. Execution must be safer than the strategy is clever
6. ML and LLM must earn their place with evidence
