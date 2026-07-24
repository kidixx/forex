"""
Candlestick pattern strategy.

Detects a handful of common reversal patterns on the most recent candles:
  - Bullish/Bearish Engulfing
  - Hammer / Shooting Star
  - Doji (treated as a neutral/no-signal warning, not a trade trigger alone)

Returns 'BUY', 'SELL', or 'HOLD'.
"""

import pandas as pd


def _body(c):
    return abs(c["close"] - c["open"])


def _range(c):
    return c["high"] - c["low"]


def _upper_wick(c):
    return c["high"] - max(c["close"], c["open"])


def _lower_wick(c):
    return min(c["close"], c["open"]) - c["low"]


def is_bullish_engulfing(prev, curr) -> bool:
    return (
        prev["close"] < prev["open"]                      # previous candle bearish
        and curr["close"] > curr["open"]                   # current candle bullish
        and curr["close"] >= prev["open"]
        and curr["open"] <= prev["close"]
    )


def is_bearish_engulfing(prev, curr) -> bool:
    return (
        prev["close"] > prev["open"]                      # previous candle bullish
        and curr["close"] < curr["open"]                   # current candle bearish
        and curr["open"] >= prev["close"]
        and curr["close"] <= prev["open"]
    )


def is_hammer(c) -> bool:
    rng = _range(c)
    if rng == 0:
        return False
    body = _body(c)
    lower = _lower_wick(c)
    upper = _upper_wick(c)
    return lower >= 2 * body and upper <= body and body / rng < 0.35


def is_shooting_star(c) -> bool:
    rng = _range(c)
    if rng == 0:
        return False
    body = _body(c)
    lower = _lower_wick(c)
    upper = _upper_wick(c)
    return upper >= 2 * body and lower <= body and body / rng < 0.35


def generate_signal(df: pd.DataFrame) -> str:
    """
    Looks at the last two closed candles for a reversal pattern.
    Hammer/bullish engulfing -> BUY. Shooting star/bearish engulfing -> SELL.
    """
    if len(df) < 3:
        return "HOLD"

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    if is_bullish_engulfing(prev, curr) or is_hammer(curr):
        return "BUY"

    if is_bearish_engulfing(prev, curr) or is_shooting_star(curr):
        return "SELL"

    return "HOLD"
