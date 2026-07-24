"""
Simple backtester — replays historical candles through the strategy
so you can see win rate / rough P&L BEFORE risking real money.

Run this first: `python backtester.py`

Note: uses fixed pip P&L approximation, not full tick-level simulation,
so treat results as directional, not exact.
"""

import mt5_connector
import strategy
import risk_manager
import config


def run_backtest(symbol: str = None, bars: int = 5000):
    symbol = symbol or config.SYMBOL
    settings = risk_manager.get_symbol_settings(symbol)
    pip_size = config.SYMBOL_SETTINGS.get(symbol, {}).get("pip_size", 0.0001)
    take_profit_pips = settings["take_profit_pips"]
    stop_loss_pips = settings["stop_loss_pips"]

    mt5_connector.connect()
    df = mt5_connector.get_candles(symbol=symbol, count=bars)
    mt5_connector.disconnect()

    trades = []
    position = None  # dict with entry info, or None

    for i in range(config.SLOW_EMA_PERIOD + 2, len(df)):
        window = df.iloc[: i + 1]
        signal = strategy.generate_signal(window)
        price = window["close"].iloc[-1]

        if position is None and signal in ("BUY", "SELL"):
            position = {"type": signal, "entry": price, "entry_i": i}
            continue

        if position is not None:
            move = (price - position["entry"]) / pip_size
            if position["type"] == "SELL":
                move = -move

            if move >= take_profit_pips:
                trades.append(take_profit_pips)
                position = None
            elif move <= -stop_loss_pips:
                trades.append(-stop_loss_pips)
                position = None

    wins = [t for t in trades if t > 0]
    losses = [t for t in trades if t < 0]
    total_pips = sum(trades)

    print(f"--- Backtest: {symbol} ---")
    print(f"Total trades: {len(trades)}")
    print(f"Wins: {len(wins)}  Losses: {len(losses)}")
    if trades:
        print(f"Win rate: {len(wins) / len(trades) * 100:.1f}%")
    print(f"Total pips: {total_pips:.1f}\n")


if __name__ == "__main__":
    for sym in config.SYMBOLS:
        run_backtest(symbol=sym)
