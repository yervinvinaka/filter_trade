import requests

from app.services.market_service import (
    calculate_ema
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

        data = requests.get(
            url,
            timeout=10
        ).json()

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

        if not closes:
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
# 🔥 MULTI TIMEFRAME ANALYSIS
# ==================================================

def analyze_multi_timeframe(symbol):

    try:

        # ==================================================
        # 🔹 1H
        # ==================================================

        closes_1h = get_tf_klines(
            symbol,
            "1h"
        )

        trend_1h = detect_trend(
            closes_1h
        )

        # ==================================================
        # 🔹 4H
        # ==================================================

        closes_4h = get_tf_klines(
            symbol,
            "4h"
        )

        trend_4h = detect_trend(
            closes_4h
        )

        # ==================================================
        # 🔹 1D
        # ==================================================

        closes_1d = get_tf_klines(
            symbol,
            "1d"
        )

        trend_1d = detect_trend(
            closes_1d
        )

        # ==================================================
        # 🔥 ALIGNMENT SCORE
        # ==================================================

        bullish_count = 0
        bearish_count = 0

        trends = [
            trend_1h,
            trend_4h,
            trend_1d
        ]

        for trend in trends:

            if trend == "BULLISH":
                bullish_count += 1

            elif trend == "BEARISH":
                bearish_count += 1

        alignment = "MIXED"

        if bullish_count >= 2:
            alignment = "BULLISH"

        elif bearish_count >= 2:
            alignment = "BEARISH"

        # ==================================================
        # 🔥 RETURN
        # ==================================================

        return {
            "1h": trend_1h,
            "4h": trend_4h,
            "1d": trend_1d,
            "alignment": alignment
        }

    except Exception as e:

        print(
            f"❌ Error multi timeframe: {e}"
        )

        return None