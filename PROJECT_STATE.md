# PROJECT_STATE.md

## Project
XAUUSD Trading Bot

## Goal
Membangun bot trading XAUUSD yang:
- valid secara research
- bebas look-ahead bias
- punya risk management ketat
- bisa naik bertahap dari research ke paper trade lalu live

## Current state

### What exists now
- Core package reusable di `src/xauusd_trading/`
- Unified data loader + OHLCV validation
- Shared indicator/feature pipeline (ATR & RSI Wilder's smoothing)
- Strategy interface tunggal minimal
- Unified backtest engine (next-bar open + spread, SL-first, prev-bar trailing)
- Risk manager (drawdown guard, consecutive-loss guard, max position cap, halt reset)
- Summary metrics module
- Trade ledger export
- Model validation (Side type, price invariants, entry_price > 0, etc.)
- Atomic state persistence (crash-safe)
- MT5 order rejection detection (retcode check)
- Risk enforcement di MT5 execution path
- Crash-proof loop scripts
- Telegram-ready alerting hook
- **FOCUS: Session basket strategies aktif** — lihat Portfolio aktif di bawah
- **Legacy single-pair strategies diarsipkan** — lihat `_archive_legacy/` dan `_archive_legacy_runners/`

### What is done now (UPDATED 2026-05-05)
- **Full audit completed**: 65 findings across 13 categories, 15 P0 fixes applied
- **Look-ahead bias eliminated**: S/R detection uses backward-only rolling + shift(1)
- **Backtest engine hardened**: next-bar-open entry, spread-as-price conversion, SL-first same-bar, prev-bar trailing, position sizing from actual risk distance
- **Risk manager enforced**: max_position_lots=10, min_risk_distance_pips parametric, pip_size per instrument
- **Parameter tuning completed**: Tested 30+ configurations across M5/M3 × 3 pairs × 3 strategies
- **2 branches profitable** (PF > 1.0): EURUSD Sweep (PF 1.01) & GBPUSD ORB (PF 1.11)
- **Risk sizing optimized**: 0.3–0.5% per trade (down from 1%) — critical for survival

### What is NOT done yet
- Belum ada risk engine terpisah yang matang untuk daily loss / exposure caps
- Belum ada execution engine production-grade
- Belum semua strategy research dimigrasikan ke core interface
- Belum ada reconcile posisi MT5 yang lengkap untuk multi-position dan stateful partial-close/trailing lifecycle lintas restart
- Belum ada live/paper runtime validation berulang di Windows RDP dengan market data MT5 yang terus bergerak
- SR+EMA V4.1 di core menguatkan kecurigaan bahwa static S/R candidate ini tetap lemah / bias-prone
- Branch M15 round 1 belum cukup robust untuk promosi, terutama karena lemah di 2022-2023 walau membaik di 2024-2026
- M15 round 2 long-only membaik, dengan kandidat terbaik sementara `m15_l2_c`, tetapi masih regime-sensitive dan belum layak promosi
- M15 round 3 quality-filter tests tidak mengalahkan `m15_l2_c`; filter mengurangi DD tetapi juga memangkas edge terlalu banyak
- M15 round 4 menemukan kandidat recent-regime yang lebih kuat, `SRSDM15LongRecentStrategy`, dengan OOS 2025-2026 tetap positif dan DD masih moderat
- M15 round 5 menghasilkan kandidat recent-regime yang lebih kuat lagi, `SRSDM15LongRecentV2Strategy`, cukup menarik untuk demo terpisah, tetapi gagal total jika dipaksa sebagai sistem all-weather 2022-2026
- Sudah ada runtime MT5 paper/demo M15 terpisah (`run_paper_trade_mt5_m15.py` dan loop) dengan state/journal/config sendiri agar tidak mengganggu jalur H1
- Sudah dimulai branch riset baru untuk EURUSD session sweep + MSS + FVG, terpisah dari family XAUUSD SR+SD
- Hasil riset awal EURUSD Jan-Apr 2026 menunjukkan M3 sudah menghasilkan setup/trade awal, sementara M5 masih nol entry, jadi M3 diprioritaskan untuk refinement berikutnya
- EURUSD session sweep round 2 menunjukkan pelonggaran ringan (`r2_a_looser_sweep`) bisa menambah trade tanpa merusak kualitas, tetapi pelonggaran displacement yang terlalu agresif langsung merusak edge
- EURUSD session sweep round 3 menunjukkan session expansion lebih efektif daripada pelonggaran filter, dengan Asia+London trigger mengalahkan Asia-only pada M3 Jan-Apr 2026
- Multi-pair round 1 menunjukkan ekspansi pair memang menambah frekuensi, tetapi GBPUSD dengan parameter copy-paste masih negatif dan USDJPY belum menghasilkan trade, jadi langkah berikutnya harus pair-specific adaptation
- GBPUSD adaptation round 1 berhasil mengubah branch GBPUSD menjadi positif lewat sweep yang lebih ketat (`min_sweep_pips=2.5`) tanpa menurunkan trade count
- Basket utama sementara EURUSD + GBPUSD adaptasi masih sehat tetapi baru sekitar 1.43 trade per minggu aktif, jadi belum memenuhi target 3 setup per minggu
- Sudah dibuka branch pattern kedua untuk session continuation + FVG sebagai sumber frekuensi tambahan yang tidak bergantung pada setup sweep-reversal saja
- Session continuation round 1 di EURUSD M3 sudah hidup dan menghasilkan trade awal yang bersih, meski frekuensinya masih rendah dan perlu diuji sebagai bagian dari basket
- Basket EURUSD dual-pattern (sweep + continuation) meningkatkan variasi setup tetapi masih hanya sekitar 1.33 trade per minggu aktif, jadi satu pair saja tetap belum cukup untuk target produktivitas
- Main basket v2 (EURUSD sweep + EURUSD continuation + GBPUSD adapted sweep) adalah basket terbaik saat ini, mencapai 3 setup pada satu minggu tetapi rata-rata masih sekitar 1.86 trade per minggu aktif
- Setelah fix bug metrik dan refresh continuation, basket gabungan sempat naik menjadi sekitar 2.00 trade per minggu aktif dan mencapai target 3 setup pada dua minggu, tetapi masih belum konsisten memenuhi target
- Penambahan XAUUSD continuation ke basket resmi meningkatkan basket menjadi 17 trade di 8 minggu aktif, rata-rata sekitar 2.125 trade per minggu aktif, dengan 3 minggu mencapai target 3 setup. XAU continuation lebih layak dipromosikan daripada XAU sweep, tetapi gap produktivitas masih tersisa
- Refinement ringan XAUUSD continuation (displacement lebih longgar, FVG lebih kecil, expiry lebih panjang) tidak mengubah hasil sama sekali. Kesimpulan sementara: bottleneck branch ini bersifat struktural, bukan sekadar threshold kecil
- Branch session ORB (opening-range breakout retest) dibuka sebagai keluarga setup ketiga. Baseline EURUSD M3 menghasilkan 64 trade, PF sekitar 1.23, return sekitar +9.08%, DD sekitar 8.72%, dan rata-rata sekitar 4.27 trade per minggu aktif. Secara raw basket frequency, penambahan ORB menaikkan basket ke sekitar 5.4 trade per minggu aktif
- Overlap review awal terhadap EURUSD sweep + continuation menunjukkan ORB tampak genuinely additive, bukan sekadar double-counting besar-besaran. Hanya sekitar 10.9% trade ORB terjadi di hari yang sama dengan branch EURUSD lama, dan hanya sekitar 4.7% trade ORB yang benar-benar overlap waktu posisi dengan branch EURUSD lain
- ORB round 2 menghasilkan tradeoff yang berguna: baseline tetap paling agresif untuk flow, `r2_b_cleaner_retest` menjadi kandidat paling seimbang untuk PF (sekitar 1.31, 44 trade, ~3.38 trade per minggu aktif), sedangkan `r2_c_wider_opening_range` memberi DD lebih rendah (~7.88%) dengan PF yang lebih lemah
- Basket round 6 yang memakai ORB `r2_b_cleaner_retest` menghasilkan sekitar 61 trade di 13 minggu aktif, rata-rata sekitar 4.69 trade per minggu aktif, dan semua 13 minggu aktif mencapai minimal 3 trade. Ini adalah titik pertama di mana target produktivitas tampak benar-benar terpecahkan tanpa harus memakai ORB baseline yang paling bising
- Realism review round 6 menunjukkan basket ini tetap kuat bahkan setelah rule eksekusi sederhana diterapkan. Dengan rule global satu posisi saja, basket masih mempertahankan 58 dari 61 trade (~95.1%) dan rata-rata sekitar 4.46 trade per minggu aktif. Dengan rule satu posisi per simbol, basket mempertahankan 60 dari 61 trade (~98.4%). Ini menurunkan kekhawatiran bahwa basket hanya terlihat bagus karena konflik eksekusi yang tidak realistis
- Priority review menunjukkan konflik aktual basket sangat kecil (hanya 3 overlap pair teramati). Rule sederhana sudah cukup: satu posisi per simbol, branch priority untuk conflict pada simbol yang sama, dan cross-symbol overlap tetap boleh. Urutan prioritas kerja saat ini: EURUSD sweep > EURUSD continuation > XAUUSD continuation > GBPUSD adapted sweep > EURUSD ORB r2_b > GBPUSD continuation
- Risk sizing review mengarah ke model tier sederhana, bukan flat 1% untuk semua branch. Rekomendasi awal: EURUSD sweep 1.00%, EURUSD continuation 0.75%, XAUUSD continuation 0.75%, GBPUSD adapted sweep 0.60%, EURUSD ORB r2_b 0.50%, GBPUSD continuation 0.25%. Intinya: ORB tetap jadi mesin flow, tapi jangan mendominasi risk budget seperti branch yang paling bersih
- Portfolio spec final v1 untuk basket session sudah ditulis di `docs/session_basket_portfolio_spec_v1.md`. Ini sekarang menjadi source of truth implementasi demo runner: branch set, priority order, one-position-per-symbol rule, cross-symbol overlap policy, risk tiers, dan guardrails awal
- Implementasi awal runner demo basket v1 sudah dibuat: `run_session_basket_demo_mt5.py` + `run_session_basket_demo_mt5_loop.py` + config sample Windows + launcher bat. Runner ini sudah menerapkan branch priority, risk tier per branch (via metadata risk override), dan one-position-per-symbol untuk paper-demo multi-symbol di MT5

## Architecture decision

### Chosen architecture now
**Research-first modular layered architecture**

Artinya:
- research script tetap dipisah dan disimpan
- core reusable logic dipindahkan bertahap ke `src/xauusd_trading/`
- belum memakai clean architecture penuh karena domain layer reusable-nya belum cukup matang
- belum memakai ML layer / LLM layer sebagai komponen utama

### Why this is realistic
Karena bottleneck utama sekarang bukan kurang AI.
Bottleneck utama adalah:
1. mencari alpha yang genuine
2. menghindari bias penelitian
3. membuat risk + execution aman
4. baru sesudah itu membangun automation yang lebih canggih

## Folder status

### Stable folders
- `research/experiments/` → historical strategy experiments
- `research/walkforward/` → no-look-ahead validation
- `research/cross_asset/` → transferability checks
- `docs/` → architecture and design notes
- `src/xauusd_trading/` → target reusable core

## Portfolio aktif (Session Basket v1)

### Strategi aktif (3 file, 6 branch)
| Branch ID | Strategy File | Pair | Risk Tier |
|-----------|--------------|------|-----------|
| `eurusd_sweep` | `eurusd_session_sweep.py` | EURUSD | 1.00% |
| `eurusd_continuation` | `session_continuation.py` | EURUSD | 0.75% |
| `eurusd_orb` | `session_orb_retest.py` | EURUSD | 0.50% |
| `gbpusd_sweep` | `eurusd_session_sweep.py` (adapted) | GBPUSD | 0.60% |
| `gbpusd_continuation` | `session_continuation.py` | GBPUSD | 0.25% |
| `xauusd_continuation` | `session_continuation.py` | XAUUSD | 0.75% |

### Branch priority (same-symbol conflict resolution)
1. `eurusd_sweep` → 2. `eurusd_continuation` → 3. `xauusd_continuation` → 4. `gbpusd_sweep` → 5. `eurusd_orb` → 6. `gbpusd_continuation`

### Active runner scripts
- `run_session_basket_demo_mt5.py` / `run_session_basket_demo_mt5_loop.py` — MT5 paper/demo
- `run_session_basket_execution_mt5.py` / `run_session_basket_execution_mt5_loop.py` — MT5 execution (dry-run default)

### Archived (legacy)
- `src/xauusd_trading/strategies/_archive_legacy/` — sr_sd_v35, sr_sd_v35_short, sr_ema_v41, tf001, m15_sr_sd
- `_archive_legacy_runners/` — run_paper_trade, run_paper_trade_mt5, run_mt5_execution, run_paper_trade_mt5_m15 (+ loops)

## Recommended next phases

### Phase A, cleanup foundation
- buat shared path/config module
- buat data loader tunggal
- buat indicator/feature module tunggal
- buat strategy interface minimal

### Phase B, core engine
- satu backtest engine reusable
- satu trade model / position model
- satu metrics/report module

### Phase C, safety
- risk caps
- drawdown guard
- kill switch
- paper-trade execution adapter

### Phase D, optional intelligence
- ML hanya bila menambah edge nyata
- LLM hanya untuk explanation, regime annotation, atau operator assistance

## Hard rules
- no look-ahead
- no hidden future leakage
- no direct jump to live before paper validation
- no overengineering before reusable core exists
- every next phase must pass audit before expanding scope
