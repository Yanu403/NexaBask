# Windows Deploy Playbook

This is a short and practical version. The focus is: **copy the project, fill in the config, set up venv, run dry-run, then go live once confident**.

## Files You Use Directly

- `runtime/paper_trade_config.windows.sample.json`
- `windows_setup_venv.bat`
- `windows_run_dry_loop.bat`
- `windows_run_live_loop.bat`
- `windows_run_m15_demo_loop.bat` (optional, separate M15 branch)
- `windows_run_session_basket_demo_loop.bat` (new, multi-symbol session basket demo)

## Ultra-Short Steps

### 1. Copy Project Folder to Windows RDP
For example, to:

```text
C:\bots\xauusd_trading\
```

### 2. Set Up Python Environment
Open Command Prompt in the project folder, then run:

```bat
windows_setup_venv.bat
```

### 3. Prepare the Real Config
Copy:

```text
runtime\paper_trade_config.windows.sample.json
```

To:

```text
runtime\paper_trade_config.json
```

Then fill in:
- Telegram bot token
- Telegram chat ID
- If Telegram HTTPS returns a cert chain error on Windows, set `telegram.insecure_ssl` to `true`
- MT5 terminal path
- MT5 login
- MT5 password
- MT5 server
- Correct broker symbol

### 4. Run Dry-run First

```bat
windows_run_dry_loop.bat
```

The goal is to:
- confirm MT5 connects
- confirm the symbol is correct
- confirm the bot can calculate signals
- confirm Telegram alerts are working
- confirm there are no unexpected tracebacks

If a Telegram error contains `CERTIFICATE_VERIFY_FAILED`, update the config:

```json
"telegram": {
  "bot_token": "...",
  "chat_id": "...",
  "insecure_ssl": true,
  "alert_all_decisions": false
}
```

By default, the execution runner now only sends alerts for important actions such as `OPEN`, `REVERSE`, `SYNC_SLTP`, or `MANAGE_POSITION`. `HOLD/NO_SIGNAL` are not sent to avoid spam.

### Optional: Run Separate M15 Demo Branch

If you want to test the latest M15 candidate without interfering with H1:

1. Copy `runtime\paper_trade_config.m15.windows.sample.json`
   to `runtime\paper_trade_config.m15.json`
2. Fill in MT5/Telegram credentials as usual
3. Run:

```bat
windows_run_m15_demo_loop.bat
```

This is a **separate M15 paper/demo loop**, not live execution.

### 5. Optional: Run Session Basket Demo Loop (Multi-Symbol)

If you want to validate the latest portfolio session (EURUSD/GBPUSD/XAUUSD) with priority + risk tier rules:

1. Copy `runtime\session_basket_demo_config.windows.sample.json`
   to `runtime\session_basket_demo_config.json`
2. Fill in broker symbols (`EURUSDm`, `GBPUSDm`, `XAUUSDm`) + credentials
3. Run:

```bat
windows_run_session_basket_demo_loop.bat
```

Detailed reference: `docs/session_basket_demo_runtime.md`

### 6. Once Dry-run Is Healthy, Go Live

```bat
windows_run_live_loop.bat
```

This script intentionally shows a warning and pauses before live send.

## Runtime File Structure That Will Be Created

- `runtime\paper_trade_config.json`
- `runtime\mt5_execution_state.json`
- `runtime\*.jsonl`

## Recommended Mode

### First Few Weeks
- Run the **dry-run loop** first
- Observe decisions and alerts over several market sessions
- Ensure the bot does not spam management actions

### Once Confident
- Switch to **live loop**
- Continue monitoring Telegram and logs

## Important Notes

- If your broker symbol is not `XAUUSD`, change it in the config, e.g. `XAUUSDm`
- Do not share `runtime\paper_trade_config.json`, as it contains secrets
- Do not delete `runtime\mt5_execution_state.json` carelessly while the bot is live, as it is part of the bot's operational memory
