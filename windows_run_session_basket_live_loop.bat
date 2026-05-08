@echo off
setlocal

if not exist .venv\Scripts\python.exe (
  echo [ERROR] .venv not found.
  echo Create it first, then install: pandas numpy MetaTrader5
  exit /b 1
)

echo [WARNING] LIVE SEND ENABLED. Orders may be sent to broker demo account.
echo.
echo ── Tip: Run in Windows Terminal for colored output ──
echo    wt.exe -d "%cd%" cmd /k "%~f0"
echo.

.venv\Scripts\python.exe run_session_basket_execution_mt5_loop.py ^
  --config runtime\session_basket_execution_config.json ^
  --interval-seconds 180 ^
  --send-telegram-alerts ^
  --allow-live-send
