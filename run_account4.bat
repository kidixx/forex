@echo off
REM ============================================================
REM Launcher for ACCOUNT 4
REM Edit the values below, then double-click this file to run.
REM Requires its own MT5 terminal installation (see setup notes
REM in the README section "Running multiple accounts").
REM ============================================================

set ACCOUNT_LABEL=account4
set MT5_LOGIN=44444444
set MT5_PASSWORD=your_account4_password
set MT5_SERVER=Exness-MT5Trial
set MT5_PATH=C:\MT5-Account4\terminal64.exe
set MAGIC_NUMBER=234004

python main.py
pause
