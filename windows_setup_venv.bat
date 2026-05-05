@echo off
setlocal
cd /d %~dp0

py -3 -m venv .venv
if errorlevel 1 (
  echo [ERROR] Failed creating virtualenv
  exit /b 1
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install pandas numpy MetaTrader5

echo.
echo [OK] Virtualenv ready.
echo Next:
echo   1. Copy runtime\paper_trade_config.windows.sample.json to runtime\paper_trade_config.json
echo   2. Fill Telegram and MT5 credentials
echo   3. Run windows_run_dry_loop.bat

endlocal
