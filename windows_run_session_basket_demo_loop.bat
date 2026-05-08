@echo off
setlocal
cd /d %~dp0

if not exist .venv\Scripts\python.exe (
  echo [ERROR] Python virtualenv not found at .venv\Scripts\python.exe
  echo Create it first, then install: pandas numpy MetaTrader5
  exit /b 1
)

REM ── Best experience: use Windows Terminal (wt.exe) for ANSI colors ──
REM If running in cmd.exe, colors will be auto-enabled via VT processing.
REM If colors still appear as raw codes, try:  wt.exe -d "%~dp0" cmd /k "%~f0"

.venv\Scripts\python.exe run_session_basket_demo_mt5_loop.py ^
  --config runtime\session_basket_demo_config.json ^
  --state-dir runtime\session_basket_states ^
  --journal-dir runtime\session_basket_journals ^
  --heartbeat-log runtime\session_basket_demo_loop.jsonl ^
  --interval-seconds 180 ^
  --send-telegram-alerts

endlocal
