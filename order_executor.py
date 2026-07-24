"""
Handles sending orders to MT5, respecting DRY_RUN mode so nothing
touches real money until you explicitly turn it off in config.py.
"""

import MetaTrader5 as mt5
import config
import risk_manager


def count_open_positions(symbol):
    """Counts this bot's open positions for a given symbol only, so each
    symbol respects MAX_OPEN_TRADES independently."""
    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        return 0
    return len([p for p in positions if p.magic == config.MAGIC_NUMBER])


def place_order(signal: str, symbol_info, account_info):
    """
    signal: 'BUY' or 'SELL'
    Sends a market order with SL/TP attached, sized by risk_manager.
    In DRY_RUN mode, logs the intended order instead of sending it.
    """
    symbol = symbol_info.name

    if count_open_positions(symbol) >= config.MAX_OPEN_TRADES:
        print(f"[{symbol}] Max open trades reached — skipping signal.")
        return None

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise RuntimeError(f"Could not get tick for {symbol}: {mt5.last_error()}")

    price = tick.ask if signal == "BUY" else tick.bid
    order_type = mt5.ORDER_TYPE_BUY if signal == "BUY" else mt5.ORDER_TYPE_SELL

    lot = risk_manager.calculate_lot_size(account_info.balance, symbol_info, symbol)
    sl, tp = risk_manager.calculate_sl_tp(signal, price, symbol_info.point, symbol)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "magic": config.MAGIC_NUMBER,
        "comment": "scalp-bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    if config.DRY_RUN:
        print(f"[DRY RUN] Would place {signal} {lot} lots {symbol} @ {price} "
              f"SL={sl} TP={tp}")
        return request

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed: retcode={result.retcode}, comment={result.comment}")
    else:
        print(f"Order placed: {signal} {lot} lots {symbol} @ {price} "
              f"SL={sl} TP={tp} (ticket {result.order})")

    return result
