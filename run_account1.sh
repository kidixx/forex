#!/bin/bash
# ============================================================
# Launcher for ACCOUNT 1 — Git Bash version
# Edit the values below, then run with: ./run_account1.sh
# Requires its own MT5 terminal installation (see README section
# "Running multiple accounts").
# ============================================================

export ACCOUNT_LABEL=account1
export MT5_LOGIN=11111111
export MT5_PASSWORD=your_account1_password
export MT5_SERVER=Exness-MT5Trial
export MT5_PATH="C:\\MT5-Account1\\terminal64.exe"
export MAGIC_NUMBER=234001

python main.py
