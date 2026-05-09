# XAUUSD Trading Bot

Bot trading XAUUSD dengan arsitektur realistis dan bertahap.

## Status snapshot

Current state project ini sudah melewati fase sekadar eksperimen liar.
Fondasi backtest, risk, reporting, MT5 paper runtime, dan MT5 execution runtime
sudah ada. Namun ini **belum boleh dianggap production bot all-weather**.

Yang sudah benar-benar ada sekarang:
- reusable backtest foundation
- risk layer dasar + guards
- MT5 paper-trade runtime
- MT5 execution runtime dengan dry-run default
- multi-symbol basket runtime awal
- Telegram alert hook opsional
- dokumentasi deploy Windows RDP / MT5

Yang belum selesai:
- broker reconciliation yang lebih matang
- restart-safe state handling yang lebih lengkap
- risk caps yang makin ketat untuk live
- validasi lintas market regime yang lebih keras
- bukti alpha yang cukup untuk menyebut sistem ini final

## Repository notes

- Repo GitHub utama bersifat **private**.
- Branch default adalah **`main`**.
- Runtime config lokal seperti `runtime/*.json` non-sample dan `.env*` memang di-ignore agar secret tidak ikut ke git.

## Current reality

Project ini belum berupa production bot modular penuh.
Saat ini isinya adalah kumpulan script riset, backtest, dan walk-forward.
Struktur sudah dirapikan agar jelas mana yang:
- riset lama
- eksperimen valid / invalid
- arah core architecture berikutnya

## Design principle

Jangan bangun sistem yang tampak canggih sebelum alpha-nya terbukti.
Urutan yang dipakai:
1. data bersih
2. signal/strategy valid, no look-ahead
3. risk management ketat
4. execution aman
5. feedback dan monitoring
6. ML bila memang terbukti membantu
7. LLM hanya sebagai lapisan pendukung, bukan inti alpha

## Directory layout

```text
projects/xauusd_trading/
├── README.md
├── PROJECT_STATE.md
├── docs/
│   ├── architecture.md
│   ├── mt5_runtime.md
│   ├── windows_deploy_checklist.md
│   └── windows_deploy_playbook.md
├── research/
│   ├── experiments/
│   │   ├── tf001/
│   │   ├── sr_sd/
│   │   └── sr_ema/
│   ├── walkforward/
│   └── cross_asset/
└── src/
    └── xauusd_trading/
        ├── config/
        ├── data/
        ├── features/
        ├── strategies/
        ├── risk/
        ├── execution/
        └── reporting/
```

## What lives where

### `research/`
Tempat script eksplorasi, backtest, dan validasi historikal.
Belum dianggap production-safe.

### `src/xauusd_trading/data/`
Nanti untuk loader data, validator, normalizer, dan source abstraction.

### `src/xauusd_trading/features/`
Nanti untuk indicators, feature engineering, regime tagging.

### `src/xauusd_trading/strategies/`
Nanti untuk rule engine atau model inference yang sudah lolos validasi.

### `src/xauusd_trading/risk/`
Nanti untuk position sizing, max exposure, drawdown guard, kill switch.

### `src/xauusd_trading/execution/`
Nanti untuk broker adapter, order lifecycle, retry, idempotency.

### `src/xauusd_trading/reporting/`
Nanti untuk trade log, metrics, monitoring, dan feedback loop.

## Current implemented foundation

Fondasi reusable awal sekarang sudah ada:
- shared data loader
- shared indicator/feature builder
- strategy interface minimal
- unified backtest engine minimal
- risk manager dasar dengan drawdown / loss guards
- summary metrics module
- trade ledger export
- single backtest entry point lewat `run_backtest.py`
- paper-trade runner awal lewat `run_paper_trade.py`
- scheduler periodik lewat `run_paper_trade_loop.py`
- MT5-connected paper-trade runner lewat `run_paper_trade_mt5.py`
- MT5-connected periodic loop lewat `run_paper_trade_mt5_loop.py`
- MT5 execution runner dengan dry-run default lewat `run_mt5_execution.py`
- MT5 execution loop runner lewat `run_mt5_execution_loop.py`
- MT5 basket execution runner (multi-symbol) lewat `run_session_basket_execution_mt5.py`
- MT5 basket execution loop runner lewat `run_session_basket_execution_mt5_loop.py`
- MT5 execution adapter sudah mendukung open, reverse, sync SL/TP dasar, serta manage-position awal (partial close + trailing-style SL sync)
- Isolated M15 research branch awal sudah ada untuk SR+SD family, tanpa mengganggu kandidat live H1
- Telegram-ready alerting hook untuk event paper trade dan execution decision

Contoh yang sudah dipindahkan ke core:
- `TF001AdjustedStrategy`
- `SRSDV35LongStrategy`
- `SREMAV41Strategy` (research comparison only, static S/R and bias-prone)

## Immediate next build target

Versi realistis berikutnya tetap bukan full ML stack.
Target berikutnya:
- validasi MT5-connected execution runner di Windows RDP
- tambah reconcile broker yang lebih matang untuk multi-position dan stateful partial management lintas restart
- lanjutkan riset M15 hanya sebagai branch terpisah bila hasil round berikutnya membaik, fokus long-only karena short-side masih lemah
- quality-filter round 3 belum mengalahkan kandidat utama saat itu
- kandidat riset M15 terdepan saat ini adalah `SRSDM15LongRecentV2Strategy`, yang cukup kuat untuk demo terpisah berbasis regime sekarang, tetapi belum valid sebagai sistem all-weather
- sudah ada runner MT5 paper/demo M15 terpisah agar observasi branch M15 tidak mengganggu runtime H1
- sudah mulai branch riset baru untuk EURUSD session sweep + MSS + FVG dengan bias M15 dan execution M5/M3
- hasil awal Jan-Apr 2026: M3 mulai menghasilkan setup dan trade kecil, M5 masih nol entry, jadi M3 jadi branch prioritas awal
- refinement terbaru menunjukkan Asia+London trigger di M3 lebih menjanjikan daripada Asia-only, tanpa perlu merusak filter kualitas
- ekspansi multi-pair awal menambah frekuensi, tetapi EURUSD tetap paling sehat; GBPUSD dan USDJPY butuh adaptasi pair-specific, bukan copy-paste parameter
- adaptasi awal GBPUSD dengan sweep lebih ketat sudah membuat branch itu positif, jadi pair-specific tuning terbukti lebih masuk akal daripada copy-paste
- basket utama sementara EURUSD + GBPUSD adaptasi sudah sehat, tetapi belum cukup produktif untuk target 3 setup per minggu
- sudah dibuka branch pattern kedua untuk session continuation + FVG, sebagai pelengkap sweep-reversal agar basket bisa menangkap hari momentum juga
- round 1 continuation di EURUSD M3 sudah menghasilkan trade awal yang bersih, jadi branch ini valid untuk diteruskan sebagai sumber setup kedua
- bahkan setelah menggabungkan sweep + continuation di EURUSD, frekuensi masih belum cukup, jadi kombinasi multi-pattern saja belum menyelesaikan target tanpa multi-pair
- basket v2 yang menggabungkan EURUSD sweep, EURUSD continuation, dan GBPUSD adapted sweep adalah yang terbaik sejauh ini, tetapi target 3 setup per minggu belum tercapai secara konsisten
- setelah refresh metrik continuation, basket gabungan kini lebih kuat dari yang sempat terlihat, namun tetap masih butuh satu sumber setup tambahan agar target mingguan lebih konsisten
- XAUUSD continuation kini menjadi kandidat basket yang layak, lebih baik daripada XAUUSD sweep, tetapi bahkan setelah ditambahkan rata-rata basket baru sekitar 2.125 trade per minggu aktif, jadi target 3 setup per minggu masih belum tercapai secara konsisten
- session basket kini sudah memiliki `docs/session_basket_portfolio_spec_v1.md` sebagai spesifikasi portfolio demo-market candidate, termasuk branch list, priority rules, conflict handling, dan risk sizing tiers
- runtime demo basket v1 sudah tersedia melalui `run_session_basket_demo_mt5.py` dan `run_session_basket_demo_mt5_loop.py` dengan panduan `docs/session_basket_demo_runtime.md`
- runtime basket execution (interaksi order ke akun MT5) tersedia via `run_session_basket_execution_mt5.py` dan `run_session_basket_execution_mt5_loop.py` (default DRY_RUN, aktif live dengan `--allow-live-send`)
- perluas risk layer ke daily loss / exposure caps bila perlu

## Notes

- Script yang terbukti look-ahead biased tetap disimpan sebagai research history, bukan sebagai basis live bot.
- Arsitektur ini mengikuti rule: simple dulu, modular saat complexity memang menuntut.
- Paper trade runner mendukung alert Telegram secara opt-in lewat `--send-telegram-alerts`, `--telegram-bot-token`, dan `--telegram-chat-id` (atau env `XAUUSD_TELEGRAM_BOT_TOKEN` / `XAUUSD_TELEGRAM_CHAT_ID`).
- Runner juga bisa baca config lokal dari `runtime/paper_trade_config.json` untuk token/chat id, dan file ini di-ignore agar secret tidak ikut ke git.
- Untuk mode periodik CSV, gunakan `run_paper_trade_loop.py --interval-seconds 300 --send-telegram-alerts`.
- Untuk runtime Windows RDP + MT5, gunakan `run_paper_trade_mt5.py` atau `run_paper_trade_mt5_loop.py`. Detail setup ada di `docs/mt5_runtime.md`.
- Untuk langkah deploy praktis ke RDP Windows, ikuti `docs/windows_deploy_checklist.md`.
- Untuk paket deploy yang lebih plug-and-play, ikuti `docs/windows_deploy_playbook.md` dan gunakan file `.bat` launcher yang disediakan.
- Untuk runtime execution periodik single-symbol di MT5, gunakan `run_mt5_execution_loop.py`.
- Untuk runtime execution periodik basket multi-symbol di MT5, gunakan `run_session_basket_execution_mt5_loop.py`.
