# MT5 Runtime Plan

Fokus deployment berikutnya adalah **Windows RDP + MT5 terminal**.

## Kenapa MT5 runtime

Untuk paper trade / live trade yang realistis, bot perlu:
- data bar yang terus update
- akses symbol broker yang benar
- jalur order/execution yang dekat dengan terminal broker
- setup yang mudah dipindah ke RDP Windows

Karena itu, arsitektur sekarang diarahkan ke:
1. strategy engine Python tetap terpisah
2. MT5 jadi data bridge, lalu nanti execution bridge
3. Telegram tetap jadi alert layer

## Komponen awal yang sudah ada

- `src/xauusd_trading/data/mt5.py`
  - init/login/shutdown MT5
  - fetch OHLCV bars dari terminal MT5
  - normalize ke DataFrame yang kompatibel dengan strategy engine sekarang
- `src/xauusd_trading/execution/mt5_execution.py`
  - snapshot posisi broker
  - build order intent dari signal
  - decision engine open / reverse / sync SLTP / manage position / hold
  - dry-run default, live send hanya kalau diaktifkan eksplisit
- `run_paper_trade_mt5.py`
  - one-shot paper-trade run langsung dari MT5 bars
- `run_paper_trade_mt5_loop.py`
  - loop periodik untuk polling MT5 bars dan kirim alert Telegram saat ada event
- `run_mt5_execution.py`
  - execution runner untuk bridge dari signal ke request MT5

## Bentuk config lokal

Tambahkan ke `runtime/paper_trade_config.json` (file ini local-only, tidak ikut git):

```json
{
  "telegram": {
    "bot_token": "...",
    "chat_id": "..."
  },
  "mt5": {
    "symbol": "XAUUSD",
    "timeframe": "H1",
    "bars": 1500,
    "terminal_path": "C:/Program Files/MetaTrader 5 terminal64.exe",
    "login": 12345678,
    "password": "...",
    "server": "Broker-Server"
  }
}
```

## Example usage

### One-shot

```bash
python run_paper_trade_mt5.py --send-telegram-alerts --json
```

### Periodic loop

```bash
python run_paper_trade_mt5_loop.py \
  --interval-seconds 300 \
  --send-telegram-alerts
```

## Important notes

- Runner ini butuh package Python `MetaTrader5` di environment Windows tempat MT5 terminal terpasang.
- `run_mt5_execution.py` sekarang sudah bisa build request execution dan baca posisi broker, tapi default-nya tetap **DRY_RUN**.
- Untuk benar-benar kirim order ke broker, harus tambahkan flag `--allow-live-send` secara eksplisit.
- Jalur execution yang sudah ada saat ini fokus pada:
  - cek posisi existing di terminal
  - build intent open posisi baru
  - reverse dengan close posisi lawan dulu bila perlu
  - sync SL/TP posisi searah bila level signal berubah material
  - manage posisi searah dengan partial close threshold dan trailing-style SL sync dasar
- Yang belum lengkap untuk production live:
  - reconcile state broker vs internal state secara penuh untuk multi-position / edge case
  - lifecycle handling yang lebih detail setelah fill
  - penyimpanan state live yang lebih kaya untuk mencegah repeated partial triggers lintas restart
