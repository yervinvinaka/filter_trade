open_trades = []


# ==================================================
# 🔥 SAVE TRADE
# ==================================================

def save_trade(
    symbol,
    signal,
    entry,
    stop_loss,
    take_profit
):

    trade = {
        "symbol": symbol,
        "signal": signal,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "status": "OPEN"
    }

    open_trades.append(trade)

    return trade


# ==================================================
# 🔥 CHECK TRADES
# ==================================================

def check_open_trades():

    return open_trades


# ==================================================
# 🔥 CLOSE TRADE
# ==================================================

def close_trade(trade, result):

    trade["status"] = result

    return trade