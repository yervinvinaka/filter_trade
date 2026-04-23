import numpy as np
from app.db.database import save_signal


def calculate_rsi(closes, period=14):
    if len(closes) < period:
        return None

    deltas = np.diff(closes)

    gains = deltas.clip(min=0)
    losses = -deltas.clip(max=0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def get_signal(rsi):
    if rsi is None:
        return None

    if rsi < 30:
        return "BUY_STRONG"
    elif rsi < 40:
        return "BUY_WEAK"
    elif rsi > 70:
        return "SELL_STRONG"
    elif rsi > 60:
        return "SELL_WEAK"

    return None


# 🔥 NUEVO: DETECCIÓN DE MOVIMIENTOS FUERTES
def detect_movement(klines):
    try:
        last = klines[-1]

        open_price = float(last[1])
        close_price = float(last[4])

        change_pct = ((close_price - open_price) / open_price) * 100

        if change_pct <= -3:
            return "DUMP", change_pct
        elif change_pct >= 3:
            return "PUMP", change_pct

        return None, change_pct

    except:
        return None, 0


def process_market_data(symbol, closes):
    rsi = calculate_rsi(closes)
    signal = get_signal(rsi)

    if signal:
        print(f"📊 {symbol} | RSI: {rsi:.2f} | Señal: {signal}")
        save_signal(symbol, signal, rsi)

    return signal