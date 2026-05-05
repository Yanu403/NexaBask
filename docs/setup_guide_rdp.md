# 🚀 Setup Guide — MT5 Demo & Live

## STEP 1: Copy Project ke RDP

Copy seluruh folder `xauusd_trading` ke RDP Windows, misalnya:
```
C:\Trading\xauusd_trading\
```

## STEP 2: Install Python di RDP

- Download Python 3.11+ dari python.org
- **PENTING:** Centang "Add Python to PATH" saat install
- Buka CMD, verify: `python --version`

## STEP 3: Install Dependencies

```cmd
cd C:\Trading\xauusd_trading
pip install pandas numpy MetaTrader5
```

## STEP 4: Setup Config

### Demo Mode
1. Copy config sample:
```cmd
copy runtime\session_basket_demo_config.windows.sample.json runtime\session_basket_demo_config.json
```

2. Edit `runtime\session_basket_demo_config.json`, isi:
```json
{
  "mt5": {
    "login": AKUN_DEMO_ANDA,
    "password": "PASSWORD_DEMO",
    "server": "BROKER_SERVER_DEMO",
    "terminal_path": "C:/Program Files/MetaTrader 5/terminal64.exe"
  },
  "telegram": {
    "bot_token": "BOT_TOKEN_ANDA",
    "chat_id": "CHAT_ID_ANDA"
  }
}
```

### Live Mode
1. Copy config sample:
```cmd
copy runtime\session_basket_execution_config.windows.sample.json runtime\session_basket_execution_config.json
```

2. Edit dengan akun **REAL** credentials

## STEP 5: Jalankan MT5

- Buka MetaTrader 5
- Login ke akun demo/real
- **Biarkan MT5 tetap terbuka** — bot butuh MT5 running

## STEP 6: Jalankan Bot

### Demo (Paper Trade — TIDAK kirim order)
```cmd
cd C:\Trading\xauusd_trading
python run_session_basket_demo_mt5.py
```

### Demo Loop (scan tiap 5 menit)
```cmd
python run_session_basket_demo_mt5_loop.py
```

Atau pakai BAT launcher:
```cmd
windows_run_session_basket_demo_loop.bat
```

### Live Execution (KIRIM ORDER REAL)
```cmd
python run_session_basket_execution_mt5.py --allow-live-send
```

### Live Loop
```cmd
python run_session_basket_execution_mt5_loop.py -- --allow-live-send
```

---

## ⚠️ SAFETY: Demo → Real Transition

### Yang Perlu Di-ubah SAJA:
1. **Config file** — Ganti credentials:
   - `login` → akun real
   - `password` → password real
   - `server` → broker server real
2. **Runner script** — Ganti dari demo ke execution runner:
   - Demo: `run_session_basket_demo_mt5_loop.py`
   - Live: `run_session_basket_execution_mt5_loop.py -- --allow-live-send`

### Safety Guards yang Sudah Ada:
- ✅ `--allow-live-send` flag — Bot **TIDAK** kirim order tanpa flag ini
- ✅ Risk manager **ENFORCED** — max drawdown 20%, max 6 consecutive losses
- ✅ Position size cap **10 lots**
- ✅ Min risk distance **3 pips** (forex) / **50 pips** (gold)
- ✅ Order rejection detection via `retcode` check
- ✅ One position per symbol rule
- ✅ Branch priority conflict resolution

### ⛔ JANGAN LANGSUNG REAL!
1. Jalankan **demo minimal 2-4 minggu** dulu
2. Pastikan signal muncul dan paper trade profit konsisten
3. Cek journal log: `runtime/session_basket_journals/`
4. Habis itu baru pertimbangkan real dengan **micro lot** (0.01)

### Checklist Sebelum Live:
- [ ] Demo berjalan 2+ minggu tanpa error
- [ ] Paper trade PnL positif atau breakeven
- [ ] Risk per trade masih 0.3-0.5% (JANGAN naikkan!)
- [ ] Telegram alerts aktif dan akurat
- [ ] MT5 connection stabil (tidak disconnect)
- [ ] Sudah test `--allow-live-send` dengan 0.01 lot dulu

---

## Branch Aktif (Tuned)

| Branch | Pair | Risk | Status |
|--------|------|------|--------|
| eurusd_sweep | EURUSD | 0.5% | ✅ Profitable (PF 1.01) |
| gbpusd_orb | GBPUSD | 0.3% | ✅ Profitable (PF 1.11) |
| eurusd_orb | EURUSD | 0.3% | ⚠️ Monitor (PF 0.63) |
| xauusd_continuation | XAUUSD | 0.3% | ⚠️ Low sample (2 trades) |

**DISABLED:** eurusd_continuation, gbpusd_sweep, gbpusd_continuation
