@echo off
REM ============================================================
REM Launcher for ACCOUNT 3
REM Edit the values below, then double-click this file to run.
REM Requires its own MT5 terminal installation (see setup notes
REM in the README section "Running multiple accounts").
REM ============================================================

set ACCOUNT_LABEL=account3
set MT5_LOGIN=33333333
set MT5_PASSWORD=your_account3_password
set MT5_SERVER=Exness-MT5Trial
set MT5_PATH=C:\MT5-Account3\terminal64.exe
set MAGIC_NUMBER=234003

python main.py
pause
