# Architecture, realistic version

## 1. What the bot should look like, realistically

Diagram yang kamu kirim bagus sebagai aspirasi, tapi untuk kondisi project sekarang versi yang realistis adalah ini:

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

Karena saat ini kita belum ada alasan kuat untuk memusatkan sistem pada:
- ML layer penuh
- LLM layer inti

Yang sudah terbukti penting justru:
- valid data
- feature yang konsisten
- backtest yang fair
- walk-forward yang fair
- risk control yang tegas
- execution yang aman

## 3. Target module responsibilities

### Data layer
Tugas:
- load CSV / broker feed
- standardize schema
- validate timestamp, duplicates, gaps, spread sanity
- isolate symbol and timeframe specific quirks

Jangan taruh:
- signal logic
- risk logic
- order placement

### Feature pipeline
Tugas:
- EMA, ATR, RSI, spread features
- candle structure
- volatility and session features
- optional regime labels

Jangan taruh:
- SL/TP rules
- broker logic

### Strategy engine
Tugas:
- consume clean features
- output setup / signal candidate
- no broker side effects
- no direct file IO if possible

Output minimal:
- side
- entry condition
- stop reference
- target reference
- reason tags

### Risk engine
Tugas:
- position sizing
- max concurrent exposure
- spread filter
- drawdown monitor
- daily loss guard
- kill switch

Ini harus menjadi gerbang keras sebelum execution.

### Execution adapter
Tugas:
- paper trade or broker order submit
- idempotent order actions
- retry rules
- fill/update/cancel handling
- persistent state and journal for runtime decisions

### Feedback / reporting
Tugas:
- trade ledger
- equity curve
- per-strategy metrics
- out-of-sample reports
- error logs and execution events

## 4. Implemented foundation, after cleanup

Sekarang fondasi reusable awal sudah ada:
- `data/loader.py` untuk load + validasi dasar data OHLCV
- `features/indicators.py` untuk EMA, ATR, RSI, session features
- `strategies/base.py` untuk interface strategy
- `strategies/tf001.py` untuk proof-of-concept strategy implementation
- `strategies/sr_sd_v35.py` untuk migrasi kandidat research kedua
- `strategies/sr_sd_v35_short.py` untuk short mirror yang refined
- `strategies/sr_ema_v41.py` untuk pembanding static S/R + EMA yang bias-prone
- `backtesting/engine.py` untuk unified backtest engine minimal
- `risk/manager.py` untuk sizing + drawdown / loss guards
- `execution/paper.py` untuk paper-trade state/journal flow
- `execution/portfolio.py` untuk candidate portfolio signal collection
- `data/mt5.py` untuk MT5 data bridge dari terminal ke strategy engine
- `reporting/metrics.py` untuk summary metrics
- `reporting/ledger.py` untuk export trade ledger
- `run_backtest.py` untuk single entry point backtest
- `run_paper_trade.py` untuk paper-trade runner kandidat portfolio berbasis CSV
- `run_paper_trade_mt5.py` untuk MT5-connected paper-trade runner
- `run_paper_trade_mt5_loop.py` untuk MT5-connected periodic runtime

Artinya project tidak lagi cuma tumpukan script eksperimen. Sudah mulai punya core reusable.

## 5. Where ML and LLM fit later

### ML, only if proven useful
ML masuk setelah baseline strategy engine sudah rapi.
Peran realistis:
- regime classifier
- probability calibration
- trade quality scoring
- feature importance study

Bukan pengganti total seluruh logic dari awal.

### LLM, not core alpha
LLM cocok nanti untuk:
- operator summary
- anomaly explanation
- strategy comparison notes
- natural language reporting
- maybe regime commentary

LLM tidak boleh jadi sumber utama entry/exit tanpa framework validasi yang sangat keras.

## 6. Suggested evolution path

### Stage 1, now
**Research-first layered**

- script riset masih ada
- common logic mulai diekstrak
- no fake abstraction

### Stage 2, when repeated logic appears
**Modular layered core**

Tambahkan reusable module untuk:
- loaders
- features
- signals
- backtest
- metrics

### Stage 3, before live trading
**Operational architecture**

Tambahkan:
- risk service/module yang lebih kaya daripada guard dasar saat ini
- execution adapter
- persistent trade log yang terhubung ke paper/live flow
- alerting and kill switch

### Stage 4, only if justified
**ML-assisted architecture**

Tambahkan ML scoring/regime layer di atas feature pipeline, bukan di atas broker secara langsung.

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
