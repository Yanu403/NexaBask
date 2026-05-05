# Windows Deploy Playbook

Ini versi singkat dan praktis. Fokusnya: **copy project, isi config, setup venv, jalankan dry-run, lalu live bila sudah yakin**.

## File yang kamu pakai langsung

- `runtime/paper_trade_config.windows.sample.json`
- `windows_setup_venv.bat`
- `windows_run_dry_loop.bat`
- `windows_run_live_loop.bat`
- `windows_run_m15_demo_loop.bat` (opsional, branch M15 terpisah)
- `windows_run_session_basket_demo_loop.bat` (baru, basket session multi-symbol demo)

## Langkah super singkat

### 1. Copy folder project ke Windows RDP
Misalnya ke:

```text
C:\bots\xauusd_trading\
```

### 2. Setup Python environment
Buka Command Prompt di folder project, lalu jalankan:

```bat
windows_setup_venv.bat
```

### 3. Siapkan config real
Copy:

```text
runtime\paper_trade_config.windows.sample.json
```

menjadi:

```text
runtime\paper_trade_config.json
```

Lalu isi:
- Telegram bot token
- Telegram chat id
- bila HTTPS Telegram error cert chain di Windows, set `telegram.insecure_ssl` ke `true`
- MT5 terminal path
- MT5 login
- MT5 password
- MT5 server
- symbol broker yang benar

### 4. Jalankan dry-run dulu

```bat
windows_run_dry_loop.bat
```

Tujuannya:
- memastikan MT5 connect
- memastikan symbol benar
- memastikan bot bisa hitung signal
- memastikan Telegram alert jalan
- memastikan tidak ada traceback aneh

Kalau error Telegram berisi `CERTIFICATE_VERIFY_FAILED`, ubah config:

```json
"telegram": {
  "bot_token": "...",
  "chat_id": "...",
  "insecure_ssl": true,
  "alert_all_decisions": false
}
```

Secara default, execution runner sekarang hanya kirim alert untuk action penting seperti `OPEN`, `REVERSE`, `SYNC_SLTP`, atau `MANAGE_POSITION`. `HOLD/NO_SIGNAL` tidak dikirim agar tidak spam.

### Opsional: jalankan branch M15 demo terpisah

Kalau ingin menguji kandidat M15 terbaru tanpa mengganggu H1:

1. Copy `runtime\paper_trade_config.m15.windows.sample.json`
   menjadi `runtime\paper_trade_config.m15.json`
2. Isi kredensial MT5/Telegram seperti biasa
3. Jalankan:

```bat
windows_run_m15_demo_loop.bat
```

Ini adalah **paper/demo loop M15** terpisah, bukan live execution.

### 5. Opsional: jalankan session basket demo loop (multi-symbol)

Kalau mau validasi portfolio session terbaru (EURUSD/GBPUSD/XAUUSD) dengan rule priority+risk tier:

1. Copy `runtime\session_basket_demo_config.windows.sample.json`
   menjadi `runtime\session_basket_demo_config.json`
2. Isi simbol broker (`EURUSDm`, `GBPUSDm`, `XAUUSDm`) + kredensial
3. Jalankan:

```bat
windows_run_session_basket_demo_loop.bat
```

Referensi detail: `docs/session_basket_demo_runtime.md`

### 6. Kalau dry-run sehat, baru live

```bat
windows_run_live_loop.bat
```

Script ini sengaja kasih warning + pause dulu sebelum live send.

## Struktur file runtime yang akan terbentuk

- `runtime\paper_trade_config.json`
- `runtime\mt5_execution_state.json`
- `runtime\*.jsonl`

## Mode yang aku sarankan

### Minggu awal
- Jalankan **dry-run loop** dulu
- lihat decision dan alert selama beberapa sesi market
- pastikan bot tidak spam management action

### Setelah percaya diri
- pindah ke **live loop**
- tetap monitor Telegram dan log

## Catatan penting

- Kalau symbol broker bukan `XAUUSD`, ganti di config, misalnya `XAUUSDm`
- Jangan share `runtime\paper_trade_config.json`, karena isinya secret
- Jangan hapus `runtime\mt5_execution_state.json` sembarangan saat bot live, karena itu bagian dari memory operasional bot
