"""
Risk management: position sizing based on account balance and pip risk,
plus stop-loss / take-profit price calculation.
"""

import config


def get_symbol_settings(symbol: str) -> dict:
    """Look up per-symbol SL/TP pip settings, falling back to EURUSD-style defaults."""
    return config.SYMBOL_SETTINGS.get(
        symbol, {"stop_loss_pips": config.STOP_LOSS_PIPS, "take_profit_pips": config.TAKE_PROFIT_PIPS}
    )


def calculate_lot_size(account_balance: float, symbol_info, symbol: str = None) -> float:
    """
    Calculate a lot size that risks no more than MAX_RISK_PERCENT of the
    account balance on this trade, given the symbol's configured stop-loss.
    Falls back to config.LOT_SIZE as a ceiling for safety.
    """
    symbol = symbol or symbol_info.name
    settings = get_symbol_settings(symbol)
    stop_loss_pips = settings["stop_loss_pips"]

    pip_value_per_lot = symbol_info.trade_tick_value * 10  # approximate pip value per standard lot
    risk_amount = account_balance * (config.MAX_RISK_PERCENT / 100)

    if pip_value_per_lot <= 0:
        return config.LOT_SIZE

    calculated_lots = risk_amount / (stop_loss_pips * pip_value_per_lot)

    # Never exceed the configured max lot size, and respect broker's minimum
    lot = min(calculated_lots, config.LOT_SIZE)
    lot = max(lot, symbol_info.volume_min)
    return round(lot, 2)


def calculate_sl_tp(order_type: str, entry_price: float, point: float, symbol: str):
    """
    Returns (stop_loss_price, take_profit_price) given the order direction,
    entry price, symbol's point size, and which symbol this is (so gold
    gets its wider pip settings instead of the forex-sized ones).
    """
    settings = get_symbol_settings(symbol)
    sl_distance = settings["stop_loss_pips"] * 10 * point
    tp_distance = settings["take_profit_pips"] * 10 * point

    if order_type == "BUY":
        sl = entry_price - sl_distance
        tp = entry_price + tp_distance
    else:  # SELL
        sl = entry_price + sl_distance
        tp = entry_price - tp_distance

    return round(sl, 5), round(tp, 5)
