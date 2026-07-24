@echo off
REM ============================================================
REM Launcher for ACCOUNT 2
REM Edit the values below, then double-click this file to run.
REM Requires its own MT5 terminal installation (see setup notes
REM in the README section "Running multiple accounts").
REM ============================================================

set ACCOUNT_LABEL=account2
set MT5_LOGIN=22222222
set MT5_PASSWORD=your_account2_password
set MT5_SERVER=Exness-MT5Trial
set MT5_PATH=C:\MT5-Account2\terminal64.exe
set MAGIC_NUMBER=234002

python main.py
pause
