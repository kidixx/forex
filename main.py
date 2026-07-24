"""
Entry point for the scalping bot.

SAFETY: config.DRY_RUN defaults to True. The bot will only simulate
orders (print them) until you deliberately set DRY_RUN = False in
config.py — and even then, start on an Exness DEMO server, not a
real-money account, until you've watched it run for a while.
"""

import time
import traceback

import config
import mt5_connector
import strategy
import order_executor


def run():
    mt5_connector.connect()

    if config.DRY_RUN:
        print("Running in DRY RUN mode — no real orders will be sent.\n")
    else:
        print("!!! LIVE MODE — real orders will be sent to your account !!!\n")

    try:
        while True:
            for symbol in config.SYMBOLS:
                try:
                    df = mt5_connector.get_candles(symbol=symbol, count=200)
                    signal = strategy.generate_signal(df)

                    if signal in ("BUY", "SELL"):
                        account_info = mt5_connector.get_account_info()
                        symbol_info = mt5_connector.get_symbol_info(symbol)
                        order_executor.place_order(signal, symbol_info, account_info)
                    else:
                        print(f"[{symbol}] No signal (HOLD) — last close {df['close'].iloc[-1]}")

                except Exception as loop_err:
                    print(f"[{symbol}] Error in trading loop: {loop_err}")
                    traceback.print_exc()

            time.sleep(config.CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nStopping bot...")
    finally:
        mt5_connector.disconnect()


if __name__ == "__main__":
    run()
