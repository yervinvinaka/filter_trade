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

    return round(rsi, 2)


# ==================================================
# 🔥 TREND FILTER
# ==================================================

def validate_trend(
    signal,
    mtf
):

    try:

        if not signal or not mtf:
            return True

        trend_4h = mtf.get("4h")

        trend_1d = mtf.get("1d")

        # ==================================================
        # 🔥 BUY FILTER
        # ==================================================

        if "BUY" in signal:

            if (
                trend_4h == "BEARISH"
                and trend_1d == "BEARISH"
            ):

                return False

        # ==================================================
        # 🔥 SELL FILTER
        # ==================================================

        elif "SELL" in signal:

            if (
                trend_4h == "BULLISH"
                and trend_1d == "BULLISH"
            ):

                return False

        return True

    except Exception as e:

        print(
            f"❌ Trend filter error: {e}"
        )

        return True


# ==================================================
# 🔥 MOMENTUM FILTER
# ==================================================

def validate_momentum(
    closes
):

    try:

        if len(closes) < 5:
            return None

        recent = closes[-5:]

        momentum = (
            recent[-1] - recent[0]
        ) / recent[0] * 100

        return round(momentum, 2)

    except Exception as e:

        print(
            f"❌ Momentum error: {e}"
        )

        return 0


# ==================================================
# 🔥 CANDLE STRENGTH
# ==================================================

def candle_strength(
    klines
):

    try:

        last = klines[-1]

        open_price = float(last[1])

        high = float(last[2])

        low = float(last[3])

        close = float(last[4])

        candle_range = high - low

        if candle_range == 0:
            return 0

        body = abs(
            close - open_price
        )

        strength = (
            body / candle_range
        ) * 100

        return round(strength, 2)

    except Exception as e:

        print(
            f"❌ Candle strength error: {e}"
        )

        return 0


# ==================================================
# 🔥 RSI + EMA SIGNAL LOGIC
# ==================================================

def get_signal(
    rsi,
    ema_signal,
    momentum,
    candle_power
):

    if rsi is None:
        return None

    # ==================================================
    # 🔥 BUY SIGNALS
    # ==================================================

    if (
        rsi <= 35
        and ema_signal == "BULLISH"
        and momentum > 0.2
        and candle_power >= 50
    ):

        return "BUY_STRONG"

    elif (
        rsi <= 40
        and momentum > 0
    ):

        return "BUY_WEAK"

    # ==================================================
    # 🔥 SELL SIGNALS
    # ==================================================

    elif (
        rsi >= 60
        and ema_signal == "BEARISH"
        and momentum < -0.2
        and candle_power >= 50
    ):

        return "SELL_STRONG"

    elif (
        rsi >= 55
        and momentum < 0
    ):

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

        volume = float(last[5])

        change_pct = (
            (
                close_price
                - open_price
            )
            / open_price
        ) * 100

        # ==================================================
        # 🔥 DUMP
        # ==================================================

        if change_pct <= -3:

            return {
                "type": "DUMP",
                "change_pct": round(
                    change_pct,
                    2
                ),
                "volume": round(
                    volume,
                    2
                )
            }

        # ==================================================
        # 🔥 PUMP
        # ==================================================

        elif change_pct >= 3:

            return {
                "type": "PUMP",
                "change_pct": round(
                    change_pct,
                    2
                ),
                "volume": round(
                    volume,
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
    klines,
    mtf=None
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
        # 🔥 MOMENTUM
        # ==================================================

        momentum = validate_momentum(
            closes
        )

        # ==================================================
        # 🔥 CANDLE POWER
        # ==================================================

        candle_power = candle_strength(
            klines
        )

        # ==================================================
        # 🔥 TRADING SIGNAL
        # ==================================================

        signal = get_signal(
            rsi,
            ema_signal,
            momentum,
            candle_power
        )

        # ==================================================
        # 🔥 TREND FILTER
        # ==================================================

        if signal and mtf:

            valid_signal = validate_trend(
                signal,
                mtf
            )

            if not valid_signal:

                print(
                    f"⛔ {symbol} | "
                    f"Signal filtrada por trend filter"
                )

                signal = None

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
            f"Momentum: {momentum}% | "
            f"Candle: {candle_power}% | "
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
            "movement": movement,
            "momentum": momentum,
            "candle_power": candle_power
        }

    except Exception as e:

        print(
            f"❌ Error procesando market data: "
            f"{e}"
        )

        return None