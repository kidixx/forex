"""
Fast entry / fast exit scalping strategy.

Logic:
  - BUY  when fast EMA crosses ABOVE slow EMA, and RSI is not overbought.
  - SELL when fast EMA crosses BELOW slow EMA, and RSI is not oversold.
  - Every trade carries a fixed pip stop-loss and take-profit (set in config)
    so exits happen fast regardless of what the indicators do next.
"""

import pandas as pd
import config
import trendline_strategy
import candlestick_strategy


def calculate_ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss.replace(0, 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def _ema_rsi_signal(df: pd.DataFrame) -> str:
    """The original EMA crossover + RSI filter signal."""
    df = df.copy()
    df["ema_fast"] = calculate_ema(df["close"], config.FAST_EMA_PERIOD)
    df["ema_slow"] = calculate_ema(df["close"], config.SLOW_EMA_PERIOD)
    df["rsi"] = calculate_rsi(df["close"], config.RSI_PERIOD)

    if len(df) < max(config.SLOW_EMA_PERIOD, config.RSI_PERIOD) + 2:
        return "HOLD"

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    crossed_up = prev["ema_fast"] <= prev["ema_slow"] and curr["ema_fast"] > curr["ema_slow"]
    crossed_down = prev["ema_fast"] >= prev["ema_slow"] and curr["ema_fast"] < curr["ema_slow"]

    if crossed_up and curr["rsi"] < config.RSI_UPPER:
        return "BUY"
    if crossed_down and curr["rsi"] > config.RSI_LOWER:
        return "SELL"

    return "HOLD"


def generate_signal(df: pd.DataFrame) -> str:
    """
    Combines three independent signals via a confluence vote:
      1. EMA crossover + RSI filter
      2. Trendline breakout
      3. Candlestick reversal pattern

    Requires at least 2 of 3 to agree on the same direction before
    triggering BUY/SELL — this keeps entries fast but filters out a lot
    of the noise any single method would act on alone.
    """
    ema_signal = _ema_rsi_signal(df)
    trend_signal = trendline_strategy.generate_signal(df)
    candle_signal = candlestick_strategy.generate_signal(df)

    votes = [ema_signal, trend_signal, candle_signal]
    buy_votes = votes.count("BUY")
    sell_votes = votes.count("SELL")

    if buy_votes >= 2:
        return "BUY"
    if sell_votes >= 2:
        return "SELL"

    return "HOLD"
