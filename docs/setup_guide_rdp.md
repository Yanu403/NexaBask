# 🚀 Setup Guide — MT5 Demo & Live

## STEP 1: Copy Project to RDP

Copy the entire `xauusd_trading` folder to your Windows RDP, for example:
```
C:\Trading\xauusd_trading\
```

## STEP 2: Install Python on RDP

- Download Python 3.11+ from python.org
- **IMPORTANT:** Check "Add Python to PATH" during installation
- Open CMD and verify: `python --version`

## STEP 3: Install Dependencies

```cmd
cd C:\Trading\xauusd_trading
pip install pandas numpy MetaTrader5
```

## STEP 4: Setup Config

### Demo Mode
1. Copy the config sample:
```cmd
copy runtime\session_basket_demo_config.windows.sample.json runtime\session_basket_demo_config.json
```

2. Edit `runtime\session_basket_demo_config.json` and fill in:
```json
{
  "mt5": {
    "login": YOUR_DEMO_ACCOUNT,
    "password": "DEMO_PASSWORD",
    "server": "DEMO_BROKER_SERVER",
    "terminal_path": "C:/Program Files/MetaTrader 5/terminal64.exe"
  },
  "telegram": {
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  }
}
```

### Live Mode
1. Copy the config sample:
```cmd
copy runtime\session_basket_execution_config.windows.sample.json runtime\session_basket_execution_config.json
```

2. Edit with your **REAL** account credentials

## STEP 5: Launch MT5

- Open MetaTrader 5
- Log in to your demo/real account
- **Keep MT5 open** — the bot requires MT5 to be running

## STEP 6: Run the Bot

### Demo (Paper Trade — Does NOT send orders)
```cmd
cd C:\Trading\xauusd_trading
python run_session_basket_demo_mt5.py
```

### Demo Loop (scans every 5 minutes)
```cmd
python run_session_basket_demo_mt5_loop.py
```

Or use the BAT launcher:
```cmd
windows_run_session_basket_demo_loop.bat
```

### Live Execution (SENDS REAL ORDERS)
```cmd
python run_session_basket_execution_mt5.py --allow-live-send
```

### Live Loop
```cmd
python run_session_basket_execution_mt5_loop.py -- --allow-live-send
```

---

## ⚠️ SAFETY: Demo → Real Transition

### What Needs to Be Changed ONLY:
1. **Config file** — Replace credentials:
   - `login` → real account
   - `password` → real password
   - `server` → real broker server
2. **Runner script** — Switch from demo to execution runner:
   - Demo: `run_session_basket_demo_mt5_loop.py`
   - Live: `run_session_basket_execution_mt5_loop.py -- --allow-live-send`

### Existing Safety Guards:
- ✅ `--allow-live-send` flag — Bot does **NOT** send orders without this flag
- ✅ Risk manager **ENFORCED** — max drawdown 20%, max 6 consecutive losses
- ✅ Position size cap **10 lots**
- ✅ Min risk distance **3 pips** (forex) / **50 pips** (gold)
- ✅ Order rejection detection via `retcode` check
- ✅ One position per symbol rule
- ✅ Branch priority conflict resolution

### ⛔ DO NOT GO LIVE IMMEDIATELY!
1. Run **demo for at least 2–4 weeks** first
2. Ensure signals appear and paper trade shows consistent profit
3. Check journal logs: `runtime/session_basket_journals/`
4. Only then consider live trading with **micro lot** (0.01)

### Pre-Live Checklist:
- [ ] Demo running 2+ weeks without errors
- [ ] Paper trade PnL positive or breakeven
- [ ] Risk per trade still at 0.3–0.5% (DO NOT increase!)
- [ ] Telegram alerts active and accurate
- [ ] MT5 connection stable (no disconnections)
- [ ] Already tested `--allow-live-send` with 0.01 lot first

---

## Active Branches (Tuned)

| Branch | Pair | Risk | Status |
|--------|------|------|--------|
| eurusd_sweep | EURUSD | 0.5% | ✅ Profitable (PF 1.01) |
| gbpusd_orb | GBPUSD | 0.3% | ✅ Profitable (PF 1.11) |
| eurusd_orb | EURUSD | 0.3% | ⚠️ Monitor (PF 0.63) |
| xauusd_continuation | XAUUSD | 0.3% | ⚠️ Low sample (2 trades) |

**DISABLED:** eurusd_continuation, gbpusd_sweep, gbpusd_continuation
