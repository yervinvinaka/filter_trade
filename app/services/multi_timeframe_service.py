import requests

from app.services.market_service import (
    calculate_ema,
    calculate_rsi
)


# ==================================================
# 🔥 GET KLINES
# ==================================================

def get_tf_klines(
    symbol,
    interval,
    limit=100
):

    try:

        url = (
            f"https://api.binance.com/api/v3/klines?"
            f"symbol={symbol}"
            f"&interval={interval}"
            f"&limit={limit}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        if not isinstance(data, list):
            return []

        closes = [
            float(k[4])
            for k in data
        ]

        return closes

    except Exception as e:

        print(
            f"❌ Error getting "
            f"{interval} klines: {e}"
        )

        return []


# ==================================================
# 🔥 TREND DETECTION
# ==================================================

def detect_trend(closes):

    try:

        if len(closes) < 21:
            return "NEUTRAL"

        ema_fast = calculate_ema(
            closes,
            9
        )

        ema_slow = calculate_ema(
            closes,
            21
        )

        if ema_fast > ema_slow:
            return "BULLISH"

        elif ema_fast < ema_slow:
            return "BEARISH"

        return "NEUTRAL"

    except Exception as e:

        print(
            f"❌ Error detect trend: {e}"
        )

        return "NEUTRAL"


# ==================================================
# 🔥 RSI ENTRY ENGINE
# ==================================================

def get_entry_signal(closes):

    try:

        if len(closes) < 20:
            return None

        rsi = calculate_rsi(
            closes
        )

        if rsi is None:
            return None

        # 🔥 MÁS FLEXIBLE

        if rsi <= 38:
            return "BUY"

        elif rsi >= 58:
            return "SELL"

        return None

    except Exception as e:

        print(
            f"❌ Error entry signal: {e}"
        )

        return None


# ==================================================
# 🔥 MULTI TIMEFRAME ANALYSIS
# ==================================================

def analyze_multi_timeframe(symbol):

    try:

        # ==================================================
        # 🔹 1H = ENTRIES
        # ==================================================

        closes_1h = get_tf_klines(
            symbol,
            "1h"
        )

        trend_1h = detect_trend(
            closes_1h
        )

        entry_signal = get_entry_signal(
            closes_1h
        )

        # ==================================================
        # 🔹 4H = MAIN TREND
        # ==================================================

        closes_4h = get_tf_klines(
            symbol,
            "4h"
        )

        trend_4h = detect_trend(
            closes_4h
        )

        # ==================================================
        # 🔹 1D = MACRO
        # ==================================================

        closes_1d = get_tf_klines(
            symbol,
            "1d"
        )

        trend_1d = detect_trend(
            closes_1d
        )

        # ==================================================
        # 🔥 ALIGNMENT
        # ==================================================

        alignment = "MIXED"

        bullish = 0
        bearish = 0

        trends = [
            trend_1h,
            trend_4h,
            trend_1d
        ]

        for trend in trends:

            if trend == "BULLISH":
                bullish += 1

            elif trend == "BEARISH":
                bearish += 1

        if bullish >= 2:
            alignment = "BULLISH"

        elif bearish >= 2:
            alignment = "BEARISH"

        # ==================================================
        # 🔥 FINAL
        # ==================================================

        return {
            "1h": trend_1h,
            "4h": trend_4h,
            "1d": trend_1d,
            "entry_signal": entry_signal,
            "alignment": alignment
        }

    except Exception as e:

        print(
            f"❌ Error multi timeframe: {e}"
        )

        return None