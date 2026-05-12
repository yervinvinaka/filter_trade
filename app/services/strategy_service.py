import numpy as np

from app.db.database import save_signal

from app.services.market_service import (
    get_ema_signal
)


# ==================================================
# 🔥 RSI CALCULATION
# ==================================================

def calculate_rsi(closes, period=14):

    if len(closes) < period:
        return None

    deltas = np.diff(closes)

    gains = deltas.clip(min=0)

    losses = -deltas.clip(max=0)

    avg_gain = np.mean(
        gains[:period]
    )

    avg_loss = np.mean(
        losses[:period]
    )

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss

    rsi = (
        100 - (100 / (1 + rs))
    )

    return rsi


# ==================================================
# 🔥 RSI + EMA SIGNAL LOGIC
# ==================================================

def get_signal(rsi, ema_signal):

    if rsi is None:
        return None

    # ==================================================
    # 🔥 BUY SIGNALS
    # ==================================================

    if (
        rsi <= 35
        and ema_signal == "BULLISH"
    ):

        return "BUY_STRONG"

    elif rsi <= 40:

        return "BUY_WEAK"

    # ==================================================
    # 🔥 SELL SIGNALS
    # ==================================================

    elif (
        rsi >= 60
        and ema_signal == "BEARISH"
    ):

        return "SELL_STRONG"

    elif rsi >= 55:

        return "SELL_WEAK"

    return None


# ==================================================
# 🔥 MOVEMENT DETECTION
# ==================================================

def detect_movement(klines):

    try:

        last = klines[-1]

        open_price = float(last[1])

        close_price = float(last[4])

        change_pct = (
            (
                close_price
                - open_price
            )
            / open_price
        ) * 100

        if change_pct <= -3:

            return {
                "type": "DUMP",
                "change_pct": round(
                    change_pct,
                    2
                )
            }

        elif change_pct >= 3:

            return {
                "type": "PUMP",
                "change_pct": round(
                    change_pct,
                    2
                )
            }

        return None

    except Exception as e:

        print(
            f"❌ Error movement detection: "
            f"{e}"
        )

        return None


# ==================================================
# 🔥 PROCESS MARKET DATA
# ==================================================

def process_market_data(
    symbol,
    closes,
    klines
):

    try:

        # ==================================================
        # 🔥 RSI
        # ==================================================

        rsi = calculate_rsi(
            closes
        )

        # ==================================================
        # 🔥 EMA SIGNAL
        # ==================================================

        ema_signal = get_ema_signal(
            closes
        )

        # ==================================================
        # 🔥 TRADING SIGNAL
        # ==================================================

        signal = get_signal(
            rsi,
            ema_signal
        )

        # ==================================================
        # 🔥 MOVEMENT DETECTION
        # ==================================================

        movement = detect_movement(
            klines
        )

        # ==================================================
        # 🔥 LOG
        # ==================================================

        rsi_value = (
            round(rsi, 2)
            if rsi
            else 0
        )

        print(
            f"📊 {symbol} | "
            f"RSI: {rsi_value} | "
            f"EMA: {ema_signal} | "
            f"Signal: {signal}"
        )

        # ==================================================
        # 🔥 SAVE SIGNAL
        # ==================================================

        if signal:

            save_signal(
                symbol,
                signal,
                rsi
            )

        # ==================================================
        # 🔥 RETURN DATA
        # ==================================================

        return {
            "signal": signal,
            "rsi": rsi,
            "ema_signal": ema_signal,
            "movement": movement
        }

    except Exception as e:

        print(
            f"❌ Error procesando market data: "
            f"{e}"
        )

        return None