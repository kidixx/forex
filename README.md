# Exness MT5 Scalping Bot

A fast-entry / fast-exit forex scalping bot using EMA crossover + RSI filter,
built for Exness via the MetaTrader5 Python package.

## Requirements

- **Windows** (MetaTrader5 Python package only works on Windows — it talks
  to a locally-running MT5 terminal)
- Python 3.9+
- MetaTrader 5 terminal installed, with your Exness account added

## Setup

1. Install MT5 terminal and log in to your Exness account (demo or real).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your credentials as environment variables (don't hardcode them):
   ```
   set MT5_LOGIN=12345678
   set MT5_PASSWORD=yourpassword
   set MT5_SERVER=Exness-MT5Trial
   ```
4. Review `config.py` and adjust strategy/risk parameters as needed.

## Recommended order of operations

1. **Backtest first**: `python backtester.py`
   Gives you a rough win rate / pip total on recent history. If this
   strategy isn't profitable historically, it's not going to become
   profitable live.
2. **Demo account**: Point `MT5_SERVER` at your Exness demo server, keep
   `DRY_RUN = True` initially, run `python main.py`, and watch the printed
   signals for a while to make sure the logic behaves as expected.
3. **Demo, live orders**: Set `DRY_RUN = False` but stay on the demo server.
   Confirm orders are placed and closed as expected, with correct SL/TP.
4. **Real money — small size**: Only after the above, switch `MT5_SERVER`
   to your real Exness server, and start with the smallest lot size
   possible. Scalping strategies are sensitive to spread and slippage —
   what works on demo may behave differently live.

## Files

- `config.py` — all credentials and tunable parameters
- `mt5_connector.py` — connects to MT5 and fetches candle data
- `strategy.py` — EMA crossover + RSI signal generation
- `risk_manager.py` — position sizing and stop-loss/take-profit calculation
- `order_executor.py` — sends orders (or logs them, in DRY_RUN mode)
- `main.py` — the live trading loop
- `backtester.py` — replay historical data through the strategy

## Running multiple accounts

The MetaTrader5 Python package can only talk to **one running terminal per
process**, so to trade multiple accounts you run **one separate MT5
terminal + one separate bot process per account**. They run fully
independently and don't interfere with each other.

1. **Install a separate MT5 terminal copy per account.**
   Don't just log a second account into your existing terminal — install
   a second copy so it has its own folder and process. Easiest way:
   copy your existing MT5 install folder to a new location
   (e.g. `C:\MT5-Account1\`, `C:\MT5-Account2\`) before installing/logging
   into the second account.

2. **Edit `run_account1.bat` and `run_account2.bat`**
   Fill in each account's login, password, server, and the path to that
   account's `terminal64.exe`. Give each a unique `MAGIC_NUMBER` so trade
   history stays distinguishable if you ever combine reporting.

3. **Run each `.bat` file** — each opens its own terminal window and
   trading loop, fully independent of the other. To add a third account,
   copy one of the `.bat` files, adjust the values, and install a third
   terminal copy the same way.

4. **For unattended running:** point each `.bat` file at from a separate
   Windows Task Scheduler entry (or separate NSSM service) so both start
   and restart independently — see the deployment notes for keeping the
   bot running when you're not at the machine.

## Important notes

- `DRY_RUN = True` by default in `config.py`. The bot will not place real
  orders until you explicitly change this.
- Scalping (tight SL/TP, fast entries) is very sensitive to spread,
  slippage, and commission — Exness spreads vary by account type
  (Standard vs Raw Spread/Zero), which will materially affect this
  strategy's real-world results versus backtest.
- This is a starting scaffold, not a finished trading system. Treat the
  EMA/RSI logic as a template to refine, not a proven strategy.
