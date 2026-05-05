@echo off
setlocal
cd /d %~dp0

if not exist .venv\Scripts\python.exe (
  echo [ERROR] Python virtualenv not found at .venv\Scripts\python.exe
  echo Create it first, then install: pandas numpy MetaTrader5
  exit /b 1
)

.venv\Scripts\python.exe run_paper_trade_mt5_m15_loop.py ^
  --config runtime\paper_trade_config.m15.json ^
  --state runtime\paper_trade_state.m15.json ^
  --journal runtime\paper_trade_journal.m15.jsonl ^
  --heartbeat-log runtime\paper_trade_mt5_m15_loop.jsonl ^
  --interval-seconds 300 ^
  --send-telegram-alerts

endlocal
