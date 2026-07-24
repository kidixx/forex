"""
Trendline breakout strategy.

Logic:
  - Find recent swing highs and swing lows (local peaks/troughs).
  - Fit a simple trendline through the last few swing highs (resistance)
    and swing lows (support).
  - BUY  when price breaks above the resistance trendline.
  - SELL when price breaks below the support trendline.
"""

import numpy as np
import pandas as pd


def find_swing_points(df: pd.DataFrame, window: int = 3):
    """
    Returns (swing_high_indices, swing_low_indices) — indices where the
    high/low is a local max/min over the given window on each side.
    """
    highs = df["high"].values
    lows = df["low"].values

    swing_highs = []
    swing_lows = []

    for i in range(window, len(df) - window):
        if highs[i] == max(highs[i - window: i + window + 1]):
            swing_highs.append(i)
        if lows[i] == min(lows[i - window: i + window + 1]):
            swing_lows.append(i)

    return swing_highs, swing_lows


def fit_trendline(indices, values):
    """Fit a straight line (slope, intercept) through the given points."""
    if len(indices) < 2:
        return None
    x = np.array(indices)
    y = np.array(values)
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept


def generate_signal(df: pd.DataFrame, lookback: int = 50) -> str:
    """
    Returns 'BUY', 'SELL', or 'HOLD' based on whether the latest close
    breaks out above/below the recent trendlines.
    """
    if len(df) < lookback + 10:
        return "HOLD"

    recent = df.iloc[-lookback:].reset_index(drop=True)
    swing_highs, swing_lows = find_swing_points(recent, window=3)

    # Use the last 3-4 swing points to fit each trendline
    resistance = fit_trendline(swing_highs[-4:], recent["high"].iloc[swing_highs[-4:]]) if len(swing_highs) >= 2 else None
    support = fit_trendline(swing_lows[-4:], recent["low"].iloc[swing_lows[-4:]]) if len(swing_lows) >= 2 else None

    last_i = len(recent) - 1
    last_close = recent["close"].iloc[-1]

    if resistance is not None:
        slope, intercept = resistance
        resistance_price = slope * last_i + intercept
        if last_close > resistance_price:
            return "BUY"

    if support is not None:
        slope, intercept = support
        support_price = slope * last_i + intercept
        if last_close < support_price:
            return "SELL"

    return "HOLD"
