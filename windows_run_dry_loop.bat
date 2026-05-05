@echo off
setlocal
cd /d %~dp0

if not exist .venv\Scripts\python.exe (
  echo [ERROR] Python virtualenv not found at .venv\Scripts\python.exe
  echo Create it first, then install: pandas numpy MetaTrader5
  exit /b 1
)

.venv\Scripts\python.exe run_mt5_execution_loop.py ^
  --config runtime\paper_trade_config.json ^
  --execution-state runtime\mt5_execution_state.json ^
  --interval-seconds 300 ^
  --send-telegram-alerts

endlocal
