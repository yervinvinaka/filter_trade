import numpy as np

from app.db.database import save_signal

from app.services.market_service import (
    get_ema_signal
)


# 🔹 RSI MANUAL
def calculate_rsi(closes, period=14):
    try:
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

    except Exception as e:
        print(f"❌ Error calculando RSI: {e}")
        return None


# 🔥 LÓGICA RSI + EMA
def get_signal(rsi, ema_signal):
    if rsi is None:
        return None

    # 🔥 LONG FUERTE
    if rsi < 25 and ema_signal in ["LONG", "BULLISH"]:
        return "BUY_STRONG"

    # 🔹 LONG DÉBIL
    elif rsi < 40 and ema_signal == "BULLISH":
        return "BUY_WEAK"

    # 🔥 SHORT FUERTE
    elif rsi > 75 and ema_signal in ["SHORT", "BEARISH"]:
        return "SELL_STRONG"

    # 🔹 SHORT DÉBIL
    elif rsi > 60 and ema_signal == "BEARISH":
        return "SELL_WEAK"

    return None


# 🔥 DETECCIÓN DE MOVIMIENTOS FUERTES
def detect_movement(klines):
    try:
        last = klines[-1]

        open_price = float(last[1])
        close_price = float(last[4])

        volume = float(last[5])

        change_pct = ((close_price - open_price) / open_price) * 100

        # 🔥 DUMP
        if change_pct <= -3:
            return {
                "type": "DUMP",
                "change_pct": round(change_pct, 2),
                "volume": volume
            }

        # 🔥 PUMP
        elif change_pct >= 3:
            return {
                "type": "PUMP",
                "change_pct": round(change_pct, 2),
                "volume": volume
            }

        return None

    except Exception as e:
        print(f"❌ Error detectando movimiento: {e}")
        return None


# 🔹 PROCESAMIENTO PRINCIPAL
def process_market_data(symbol, closes, klines):
    try:
        rsi = calculate_rsi(closes)

        ema_signal = get_ema_signal(closes)

        signal = get_signal(rsi, ema_signal)

        movement = detect_movement(klines)

        # 🔥 CORRECCIÓN DEL ERROR
        rsi_value = round(rsi, 2) if rsi else 0

        # 🔹 LOG PRINCIPAL
        print(
            f"📊 {symbol} | "
            f"RSI: {rsi_value} | "
            f"EMA: {ema_signal} | "
            f"Signal: {signal}"
        )

        # 🔥 ALERTA MOVIMIENTO FUERTE
        if movement:
            print(
                f"🚨 {movement['type']} detectado en {symbol} | "
                f"Cambio: {movement['change_pct']}%"
            )

        # 🔹 GUARDAR SEÑAL
        if signal:
            save_signal(symbol, signal, rsi)

        return {
            "signal": signal,
            "rsi": rsi,
            "ema_signal": ema_signal,
            "movement": movement
        }

    except Exception as e:
        print(f"❌ Error procesando market data: {e}")
        return None