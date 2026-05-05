# M15 Demo Runtime

Jalur ini dibuat **terpisah dari H1**.
Tujuannya bukan mengganti branch H1, tapi menguji kandidat **`SRSDM15LongRecentV2Strategy`** sebagai eksperimen demo berbasis regime sekarang.

## File utama

- `run_paper_trade_mt5_m15.py`
- `run_paper_trade_mt5_m15_loop.py`
- `runtime/paper_trade_config.m15.windows.sample.json`
- `windows_run_m15_demo_loop.bat`

## Sifat branch ini

- timeframe default: `M15`
- strategy: `SRSDM15LongRecentV2Strategy`
- mode: **paper/demo only**
- state, journal, dan heartbeat dipisahkan dari H1

## File runtime default

- state: `runtime/paper_trade_state.m15.json`
- journal: `runtime/paper_trade_journal.m15.jsonl`
- heartbeat: `runtime/paper_trade_mt5_m15_loop.jsonl`
- config: `runtime/paper_trade_config.m15.json`

## Setup di Windows

1. Copy `runtime/paper_trade_config.m15.windows.sample.json`
   menjadi `runtime/paper_trade_config.m15.json`
2. Isi kredensial MT5 dan Telegram
3. Pastikan symbol broker benar dan history M15 sudah tersedia di MT5
4. Jalankan:

```bat
windows_run_m15_demo_loop.bat
```

## Catatan penting

- Ini **tidak** memakai file state/journal H1
- Ini **tidak** mengirim order live
- Ini sengaja dipisah supaya observasi M15 tidak merusak runtime H1 yang sudah ada
- Kandidat ini **regime-specific**, bukan sistem all-weather 2022-2026

## Saran operasional

- Jalankan paralel dengan H1 hanya kalau resource Windows RDP aman
- Cek log heartbeat apakah event M15 terlalu sering/noisy
- Jangan promosi ke live send sebelum perilaku demo cukup bersih selama beberapa hari
