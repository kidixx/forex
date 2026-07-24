"""
Configuration for the scalping bot.
NEVER commit real credentials to source control — use environment variables
in production. Placeholder values are shown here for clarity.
"""

import os

# --- MT5 / Exness account credentials ---
MT5_LOGIN = int(os.getenv("MT5_LOGIN", "0"))          # Your Exness MT5 account number
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")           # Your MT5 account password
MT5_SERVER = os.getenv("MT5_SERVER", "Exness-MT5Trial")  # e.g. "Exness-MT5Real" or "Exness-MT5Trial"
MT5_PATH = os.getenv("MT5_PATH", "")                   # Path to THIS account's terminal64.exe. REQUIRED when
                                                         # running multiple accounts — each account needs its own
                                                         # separate MT5 terminal installation to connect to.

# --- Multi-account labeling (optional but recommended) ---
ACCOUNT_LABEL = os.getenv("ACCOUNT_LABEL", "default")   # Friendly name shown in logs/console, e.g. "account1"

# --- Trading parameters ---
SYMBOLS = ["EURUSD", "XAUUSD"]   # Pairs to trade — XAUUSD is spot gold
SYMBOL = SYMBOLS[0]              # kept for backward compatibility with single-symbol calls
TIMEFRAME = "M1"                 # M1 = 1 minute candles, good for scalping
LOT_SIZE = 0.01                  # Start small — 0.01 lot = micro lot

# Gold moves in bigger raw price increments than forex pairs, so it gets
# its own pip-equivalent risk settings. "Pip" here means a $0.10 move.
SYMBOL_SETTINGS = {
    "EURUSD": {"stop_loss_pips": 8, "take_profit_pips": 12, "pip_size": 0.0001},
    "XAUUSD": {"stop_loss_pips": 50, "take_profit_pips": 80, "pip_size": 0.01},
}

# --- Strategy parameters (fast entry / fast exit) ---
FAST_EMA_PERIOD = 5
SLOW_EMA_PERIOD = 13
RSI_PERIOD = 14
RSI_UPPER = 70             # Avoid buying above this (overbought)
RSI_LOWER = 30             # Avoid selling below this (oversold)

# --- Risk management ---
STOP_LOSS_PIPS = 8         # Tight stop for scalping
TAKE_PROFIT_PIPS = 12      # Fast exit target
# WARNING: 10% risk per trade is still aggressive relative to the 0.5-2%
# most traders use — a run of 4-5 losing trades (normal in scalping) would
# still cost roughly half the account. Set to 10% at your request.
MAX_RISK_PERCENT = 10.0
MAX_OPEN_TRADES = 1        # Keep it simple — one position at a time to start
MAGIC_NUMBER = int(os.getenv("MAGIC_NUMBER", "234000"))  # Unique ID to identify this bot's trades.
                                                           # Give each account its own value (e.g. 234001,
                                                           # 234002) so trade history stays distinguishable
                                                           # if you ever consolidate reporting across accounts.

# --- Bot behavior ---
CHECK_INTERVAL_SECONDS = 5   # How often to check for new signals
DRY_RUN = True                # IMPORTANT: True = simulate only, no real orders sent
