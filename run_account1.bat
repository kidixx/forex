@echo off
REM ============================================================
REM Launcher for ACCOUNT 1
REM Edit the values below, then double-click this file to run.
REM Requires its own MT5 terminal installation (see setup notes
REM in the README section "Running multiple accounts").
REM ============================================================

set ACCOUNT_LABEL=account1
set MT5_LOGIN=11111111
set MT5_PASSWORD=your_account1_password
set MT5_SERVER=Exness-MT5Trial
set MT5_PATH=C:\MT5-Account1\terminal64.exe
set MAGIC_NUMBER=234001

python main.py
pause
