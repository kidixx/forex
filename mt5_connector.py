"""
Handles connecting to the MT5 terminal and fetching market data.
Requires the MetaTrader5 terminal to be installed and logged in
(or credentials supplied here), and only runs on Windows.
"""

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import config


TIMEFRAME_MAP = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "H1": mt5.TIMEFRAME_H1,
}


def connect():
    """Initialize connection to MT5 terminal and log in to the Exness account."""
    kwargs = {}
    if config.MT5_PATH:
        kwargs["path"] = config.MT5_PATH

    if not mt5.initialize(**kwargs):
        raise RuntimeError(f"MT5 initialize() failed: {mt5.last_error()}")

    authorized = mt5.login(
        login=config.MT5_LOGIN,
        password=config.MT5_PASSWORD,
        server=config.MT5_SERVER,
    )
    if not authorized:
        mt5.shutdown()
        raise RuntimeError(f"MT5 login failed: {mt5.last_error()}")

    print(f"[{datetime.now()}] [{config.ACCOUNT_LABEL}] Connected to MT5 — "
          f"account {config.MT5_LOGIN} on {config.MT5_SERVER}")


def disconnect():
    mt5.shutdown()
    print(f"[{datetime.now()}] [{config.ACCOUNT_LABEL}] Disconnected from MT5")


def get_candles(symbol=config.SYMBOL, timeframe=config.TIMEFRAME, count=200):
    """Fetch recent candle data as a pandas DataFrame."""
    tf = TIMEFRAME_MAP.get(timeframe, mt5.TIMEFRAME_M1)
    rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
    if rates is None or len(rates) == 0:
        raise RuntimeError(f"No candle data returned for {symbol}: {mt5.last_error()}")

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df


def get_account_info():
    info = mt5.account_info()
    if info is None:
        raise RuntimeError(f"Failed to get account info: {mt5.last_error()}")
    return info


def get_symbol_info(symbol=config.SYMBOL):
    info = mt5.symbol_info(symbol)
    if info is None:
        raise RuntimeError(f"Symbol {symbol} not found: {mt5.last_error()}")
    if not info.visible:
        mt5.symbol_select(symbol, True)
    return info
