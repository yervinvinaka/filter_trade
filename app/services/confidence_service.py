# ==================================================
# 🔥 CONFIDENCE ENGINE
# ==================================================

def calculate_confidence(

    signal,
    rsi,
    ema_signal,
    funding,
    alignment=None,
    volatility=None,
    movement=None

):

    try:

        score = 0

        # ==================================================
        # 🔹 RSI SCORE
        # ==================================================

        if rsi:

            # BUY

            if "BUY" in signal:

                if rsi <= 30:
                    score += 25

                elif rsi <= 38:
                    score += 15

            # SELL

            elif "SELL" in signal:

                if rsi >= 70:
                    score += 25

                elif rsi >= 58:
                    score += 15

        # ==================================================
        # 🔹 EMA SCORE
        # ==================================================

        bullish_signals = [
            "LONG",
            "BULLISH"
        ]

        bearish_signals = [
            "SHORT",
            "BEARISH"
        ]

        if (

            "BUY" in signal
            and ema_signal in bullish_signals

        ):

            score += 25

        elif (

            "SELL" in signal
            and ema_signal in bearish_signals

        ):

            score += 25

        # ==================================================
        # 🔹 MULTI TIMEFRAME SCORE
        # ==================================================

        if alignment:

            if (

                "BUY" in signal
                and alignment == "BULLISH"

            ):

                score += 20

            elif (

                "SELL" in signal
                and alignment == "BEARISH"

            ):

                score += 20

        # ==================================================
        # 🔹 FUNDING SCORE
        # ==================================================

        if (

            "BUY" in signal
            and funding < 0

        ):

            score += 15

        elif (

            "SELL" in signal
            and funding > 0

        ):

            score += 15

        # ==================================================
        # 🔹 VOLATILITY SCORE
        # ==================================================

        if volatility:

            if volatility["score"] >= 60:

                score += 20

            elif volatility["score"] >= 30:

                score += 10

        # ==================================================
        # 🔹 MOVEMENT SCORE
        # ==================================================

        if movement:

            movement_type = movement[0]

            if movement_type in [
                "PUMP",
                "DUMP"
            ]:

                score += 15

        # ==================================================
        # 🔥 LIMIT
        # ==================================================

        if score > 100:
            score = 100

        # ==================================================
        # 🔥 LEVEL
        # ==================================================

        if score >= 80:

            level = "HIGH"

        elif score >= 60:

            level = "MEDIUM"

        else:

            level = "LOW"

        return {

            "score": score,

            "level": level

        }

    except Exception as e:

        print(
            f"❌ Error confidence engine: {e}"
        )

        return {

            "score": 0,

            "level": "LOW"

        }


# ==================================================
# 🔥 SETUP CLASSIFICATION
# ==================================================

def get_setup_type(

    signal,
    ema_signal,
    alignment=None

):

    try:

        if not signal:
            return "NO_SETUP"

        # ==================================================
        # 🔹 TREND CONTINUATION
        # ==================================================

        if (

            "BUY" in signal
            and ema_signal == "BULLISH"
            and alignment == "BULLISH"

        ):

            return "TREND_CONTINUATION"

        if (

            "SELL" in signal
            and ema_signal == "BEARISH"
            and alignment == "BEARISH"

        ):

            return "TREND_CONTINUATION"

        # ==================================================
        # 🔹 COUNTER TREND
        # ==================================================

        if (

            "BUY" in signal
            and ema_signal == "BEARISH"

        ):

            return "COUNTER_TREND"

        if (

            "SELL" in signal
            and ema_signal == "BULLISH"

        ):

            return "COUNTER_TREND"

        # ==================================================
        # 🔹 DEFAULT
        # ==================================================

        return "MIXED_SETUP"

    except Exception as e:

        print(
            f"❌ Setup type error: {e}"
        )

        return "UNKNOWN"