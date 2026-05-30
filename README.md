     1|<div align="center">
     2|
     3|# ⚡ NexaBask
     4|
     5|**Production-grade basket trading system with risk-first architecture**
     6|
     7|![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
     8|![License](https://img.shields.io/badge/License-MIT-green)
     9|![Architecture](https://img.shields.io/badge/Architecture-Modular-orange)
    10|![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)
    11|
    12|[Architecture](docs/architecture.md) · [Deployment Guide](docs/windows_deploy_playbook.md) · [Portfolio Spec](docs/session_basket_portfolio_spec_v1.md) · [Research Reports](docs/reports/)
    13|
    14|</div>
    15|
    16|---
    17|
    18|## What Is This?
    19|
    20|A modular, research-driven basket trading system for XAUUSD (Gold) and forex pairs, built around a single principle: **prove the alpha before building the system**.
    21|
    22|Unlike typical trading bots that jump straight to execution, this project follows a disciplined research-first workflow — clean data → validated signals → strict risk management → safe execution → feedback loop → optional ML/LLM augmentation.
    23|
    24|### Key Highlights
    25|
    26|- 🔬 **Walk-forward validated** — every strategy passes out-of-sample testing before promotion
    27|- 🛡️ **Risk-first design** — drawdown guards, kill switches, position sizing, and daily loss caps enforced at the engine level
    28|- 📊 **Multi-strategy basket portfolio** — 6 strategy branches across 3 pairs with priority-based conflict resolution
    29|- 🔄 **MT5 integration** — paper trading, demo, and live execution via MetaTrader 5
    30|- 📱 **Telegram alerting** — optional real-time notifications for trade events
    31|- 🧪 **Audit-driven development** — 65-point audit completed, 15 critical fixes applied
    32|- 🤖 **ML/LLM roadmap** — planned integration for regime detection, feature engineering, and trade analysis
    33|
    34|---
    35|
    36|## Architecture
    37|
    38|```
    39|Market Data
    40|    │
    41|    ▼
    42|┌─────────────────────┐
    43|│  Data Validation &   │  ← OHLCV cleaning, gap detection, spread sanity
    44|│  Normalization       │
    45|└─────────┬───────────┘
    46|          │
    47|          ▼
    48|┌─────────────────────┐
    49|│  Feature Pipeline    │  ← ATR, RSI, session features, candle structure
    50|└─────────┬───────────┘
    51|          │
    52|          ▼
    53|┌─────────────────────┐
    54|│  Strategy Engine     │  ← Signal candidates with entry/SL/TP + reason tags
    55|└─────────┬───────────┘
    56|          │
    57|          ▼
    58|┌─────────────────────┐
    59|│  Risk Engine         │  ← Position sizing, exposure caps, drawdown guard, kill switch
    60|└─────────┬───────────┘
    61|          │
    62|          ▼
    63|┌─────────────────────┐
    64|│  Execution Adapter   │  ← Paper / MT5 dry-run / MT5 live, with idempotent order handling
    65|└─────────┬───────────┘
    66|          │
    67|          ▼
    68|┌─────────────────────┐
    69|│  Reporting &         │  ← Trade ledger, metrics, Telegram alerts, feedback loop
    70|│  Monitoring          │
    71|└─────────────────────┘
    72|```
    73|
    74|Each layer is independent. The strategy engine never touches broker logic. The risk engine is a hard gate before any execution. The execution adapter supports paper → dry-run → live promotion without code changes.
    75|
    76|---
    77|
    78|## Portfolio: Session Basket v1
    79|
    80|The active portfolio uses **session-based strategies** — setups triggered by London/NY session dynamics across multiple forex pairs.
    81|
    82|| Branch | Strategy | Pair | Risk/Trade | Role |
    83||--------|----------|------|-----------|------|
    84|| `eurusd_sweep` | Session Sweep + FVG | EURUSD | 1.00% | Primary alpha |
    85|| `eurusd_continuation` | Session Continuation | EURUSD | 0.75% | Momentum capture |
    86|| `eurusd_orb` | Opening Range Breakout | EURUSD | 0.50% | Flow engine |
    87|| `gbpusd_sweep` | Session Sweep (adapted) | GBPUSD | 0.60% | Cross-pair expansion |
    88|| `gbpusd_continuation` | Session Continuation | GBPUSD | 0.25% | Supplementary |
    89|| `xauusd_continuation` | Session Continuation | XAUUSD | 0.75% | Gold momentum |
    90|
    91|**Conflict resolution:** One position per symbol, branch priority ordering, cross-symbol overlap allowed.
    92|
    93|**Latest basket performance:** ~4.5 setups/week across all branches, with 95%+ survival rate under single-position execution constraints.
    94|
    95|---
    96|
    97|## Project Structure
    98|
    99|```
   100|├── src/nexabask/          # Core reusable package
   101|│   ├── backtesting/             # Unified backtest engine (next-bar open, spread-aware)
   102|│   ├── config/                  # Path management, config loading
   103|│   ├── execution/               # MT5 adapter, paper trade, portfolio runner, alerts
   104|│   ├── features/                # Indicators (ATR, RSI Wilder's), feature builder
   105|│   ├── models/                  # Trade/position models (live, paper, trading)
   106|│   ├── reporting/               # Metrics, trade ledger export
   107|│   ├── risk/                    # Risk manager (drawdown, consecutive loss, position cap)
   108|│   └── strategies/              # Strategy implementations + base interface
   109|│
   110|├── research/                    # Experiments, walk-forward validation, cross-asset
   111|│   ├── experiments/             # Strategy-specific research (EURUSD sweep, M15, etc.)
   112|│   └── walkforward/             # No-look-ahead validation scripts
   113|│
   114|├── docs/                        # Architecture, specs, deploy guides, audit reports
   115|│   └── reports/                 # Per-round backtest & basket analysis reports
   116|│
   117|├── runtime/                     # Sample configs (secrets excluded via .gitignore)
   118|├── tests/                       # Test suite
   119|│
   120|├── run_session_basket_demo_mt5.py      # MT5 paper/demo runner
   121|├── run_session_basket_execution_mt5.py # MT5 execution runner (dry-run default)
   122|├── run_basket_backtest.py              # Portfolio-level backtest
   123|└── windows_*.bat                       # Windows RDP launchers
   124|```
   125|
   126|---
   127|
   128|## Getting Started
   129|
   130|### Prerequisites
   131|
   132|- Python 3.11+
   133|- For MT5 integration: Windows with [MetaTrader 5](https://www.metatrader5.com/) installed
   134|
   135|### Installation
   136|
   137|```bash
   138|git clone https://github.com/Yanu403/xauusd_trading.git
   139|cd xauusd_trading
   140|pip install -r requirements.txt
   141|```
   142|
   143|### Run a Backtest
   144|
   145|```bash
   146|python run_basket_backtest.py
   147|```
   148|
   149|### Run Paper Trading (CSV mode)
   150|
   151|```bash
   152|python run_paper_trade.py --send-telegram-alerts
   153|```
   154|
   155|### Run MT5 Paper/Demo (Windows)
   156|
   157|```bash
   158|python run_session_basket_demo_mt5_loop.py
   159|```
   160|
   161|### Run MT5 Execution (Windows, dry-run by default)
   162|
   163|```bash
   164|python run_session_basket_execution_mt5_loop.py
   165|# Add --allow-live-send to enable real order submission
   166|```
   167|
   168|> 📖 See [Windows Deployment Playbook](docs/windows_deploy_playbook.md) for full setup instructions.
   169|
   170|---
   171|
   172|## Design Philosophy
   173|
   174|### Why No ML/LLM Yet?
   175|
   176|This project follows a strict dependency chain:
   177|
   178|```
   179|1. Clean data
   180|2. Valid signal — no look-ahead bias
   181|3. Strict risk management
   182|4. Safe execution
   183|5. Feedback & monitoring
   184|6. ML only if it provably adds edge
   185|7. LLM only as support layer (trade journal, regime annotation)
   186|```
   187|
   188|Building ML infrastructure before proving alpha is engineering theater. The current priority is validating the basket portfolio under live market conditions.
   189|
   190|### Hard Rules
   191|
   192|- ❌ No look-ahead bias (enforced via backward-only rolling + shift(1))
   193|- ❌ No hidden future leakage
   194|- ❌ No live trading before paper validation
   195|- ❌ No overengineering before reusable core exists
   196|- ✅ Every phase must pass audit before expanding scope
   197|
   198|---
   199|
   200|## Roadmap
   201|
   202|### ✅ Phase A — Foundation (Done)
   203|- Shared data loader, indicator pipeline, strategy interface
   204|- Unified backtest engine with realistic execution modeling
   205|- Risk manager with drawdown guards and kill switch
   206|
   207|### ✅ Phase B — Core Engine (Done)
   208|- Trade/position models
   209|- Metrics and trade ledger
   210|- Atomic state persistence (crash-safe)
   211|
   212|### ✅ Phase C — Safety Layer (Done)
   213|- MT5 execution adapter with dry-run default
   214|- Portfolio-level conflict resolution
   215|- Telegram alerting hook
   216|
   217|### 🔄 Phase D — Production Hardening (In Progress)
   218|- Broker reconciliation for multi-position stateful management
   219|- Restart-safe state handling across process crashes
   220|- Tighter risk caps for live deployment
   221|- Cross-regime validation (2022-2026 stress testing)
   222|
   223|### 🔮 Phase E — Intelligence Layer (Planned)
   224|- **ML Feature Engineering** — regime detection, volatility clustering, session classification
   225|- **ML Signal Enhancement** — model-augmented entry/exit timing (only if proven via walk-forward)
   226|- **LLM Trade Analysis** — automated trade journaling, performance commentary, anomaly explanation
   227|- **LLM Operator Assistant** — natural language query over trade history and risk metrics
   228|
   229|### 🌐 Phase F — Expansion (Planned)
   230|- Multi-pair scaling with pair-specific parameter optimization
   231|- Web dashboard for portfolio monitoring
   232|- REST API for external signal consumption
   233|- Backtest-as-a-service for strategy research
   234|
   235|---
   236|
   237|## Research Methodology
   238|
   239|Every strategy goes through a rigorous validation pipeline:
   240|
   241|1. **Hypothesis** — define the market behavior being exploited
   242|2. **Implementation** — code the strategy with strict no-look-ahead rules
   243|3. **In-sample backtest** — initial validation on training data
   244|4. **Walk-forward validation** — out-of-sample testing on unseen data
   245|5. **Audit** — bias detection, execution realism, risk sizing review
   246|6. **Basket integration** — portfolio-level conflict and overlap analysis
   247|7. **Paper trading** — live market validation via MT5 demo
   248|8. **Promotion** — only after all gates pass
   249|
   250|Research reports for each round are preserved in [`docs/reports/`](docs/reports/) for full transparency.
   251|
   252|---
   253|
   254|## Contributing
   255|
   256|Contributions are welcome. Please read the [architecture docs](docs/architecture.md) before submitting changes.
   257|
   258|Areas where help is especially valuable:
   259|- Strategy research (new session patterns, additional pairs)
   260|- ML feature engineering for regime detection
   261|- Risk management improvements
   262|- Documentation and testing
   263|
   264|---
   265|
   266|## Disclaimer
   267|
   268|⚠️ **This is a research project, not financial advice.** Trading forex and gold involves substantial risk of loss. The strategies in this repository have not been proven profitable in live trading. Use at your own risk. Past backtest performance does not guarantee future results.
   269|
   270|---
   271|
   272|## License
   273|
   274|[MIT](LICENSE) — use it, fork it, learn from it.
   275|
   276|---
   277|
   278|<div align="center">
   279|
   280|**NexaBask** — Built with discipline, not hype.
   281|
   282|*"Don't build a sophisticated system before the alpha is proven."*
   283|
   284|</div>
   285|