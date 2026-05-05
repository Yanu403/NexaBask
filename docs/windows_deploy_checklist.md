# Windows RDP Deploy Checklist

Tujuan dokumen ini: bikin deploy MT5 runtime jadi **plug and play** semaksimal mungkin.

## 1. Install dasar di Windows RDP

- Install **Python 3.11+**
- Install **MetaTrader 5 terminal**
- Login ke account broker di terminal MT5
- Pastikan symbol yang dipakai memang tersedia, misalnya `XAUUSD` atau `XAUUSDm`

## 2. Siapkan project

Copy folder `projects/xauusd_trading/` ke Windows RDP.

Kalau mau jalur paling praktis, langsung pakai juga:
- `windows_setup_venv.bat`
- `windows_run_dry_loop.bat`
- `windows_run_live_loop.bat`
- `runtime/paper_trade_config.windows.sample.json`

Struktur minimal yang harus ada:

```text
xauusd_trading/
├── run_paper_trade_mt5.py
├── run_paper_trade_mt5_loop.py
├── run_mt5_execution.py
├── run_mt5_execution_loop.py
├── runtime/
│   ├── paper_trade_config.json
│   └── ...state files...
└── src/
```

## 3. Install dependencies Python

Disarankan install ini di virtual environment:

```bash
pip install pandas numpy MetaTrader5
```

## 4. Isi config runtime lokal

Edit file:

`runtime/paper_trade_config.json`

Cara tercepat:
1. copy `runtime/paper_trade_config.windows.sample.json`
2. rename jadi `runtime/paper_trade_config.json`
3. isi credential real

Pastikan section berikut benar:

- `telegram.bot_token`
- `telegram.chat_id`
- `telegram.insecure_ssl` bila environment Windows bermasalah di SSL Telegram
- `telegram.alert_all_decisions` jika kamu memang ingin semua decision, termasuk `HOLD`, ikut dikirim
- `mt5.symbol`
- `mt5.timeframe`
- `mt5.terminal_path`
- `mt5.login`
- `mt5.password`
- `mt5.server`
- `execution.lot_step`
- `execution.min_lot`
- `execution.max_lot`

## 5. Test bertahap, jangan lompat ke live

### Step A, cek help

```bash
python run_mt5_execution.py --help
```

### Step B, dry-run execution

```bash
python run_mt5_execution.py --json
```

Yang dicek:
- MT5 bisa connect
- data bisa diambil
- signal bisa dihitung
- decision keluar normal
- tidak ada traceback

### Step C, dry-run berkala

Gunakan runtime MT5 paper loop untuk lihat alur berulang.

### Step D, execution loop dry-run

```bash
python run_mt5_execution_loop.py --interval-seconds 300 --json
```

### Step E, baru live sangat hati-hati

```bash
python run_mt5_execution.py --allow-live-send --send-telegram-alerts --json
```

Atau untuk mode jalan terus:

```bash
python run_mt5_execution_loop.py --interval-seconds 300 --allow-live-send --send-telegram-alerts
```

## 6. File runtime penting

- `runtime/paper_trade_config.json`
- `runtime/mt5_execution_state.json`
- `runtime/*.jsonl`

### Kenapa `mt5_execution_state.json` penting

File ini menyimpan state live management seperti:
- partial close sudah pernah dilakukan atau belum
- sync SL/TP terakhir

Tanpa file ini, bot bisa lebih mudah mengulang aksi management setelah restart.

## 7. Rekomendasi mode jalan awal

Urutan paling aman:
1. `run_paper_trade_mt5.py`
2. `run_paper_trade_mt5_loop.py`
3. `run_mt5_execution.py` tanpa `--allow-live-send`
4. `run_mt5_execution_loop.py` tanpa `--allow-live-send`
5. `run_mt5_execution.py` atau `run_mt5_execution_loop.py` dengan `--allow-live-send`

## 8. Sebelum live pertama

Checklist final:
- [ ] Symbol broker sudah benar
- [ ] Lot step cocok dengan broker
- [ ] Account yang dipakai memang account yang benar
- [ ] Telegram alert masuk normal
- [ ] Dry-run decision terlihat masuk akal
- [ ] MT5 terminal stabil dan tidak minta login ulang
- [ ] VPS/RDP timezone dipahami dengan benar
- [ ] State file runtime tidak ikut sinkronisasi aneh atau tertimpa

## 9. Catatan jujur

Runtime ini sudah cukup kuat untuk validasi serius, tapi belum final sempurna.
Yang masih perlu diawasi ketat saat awal live:
- multi-position edge case
- repeated management setelah kondisi broker berubah cepat
- trailing/partial lifecycle yang lebih kompleks
