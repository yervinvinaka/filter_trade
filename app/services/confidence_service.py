def calculate_confidence(
    signal,
    rsi,
    ema_signal,
    funding,
    volatility=None,
    movement=None
):

    try:

        score = 0

        # ==================================================
        # RSI SCORE
        # ==================================================

        if rsi:

            # BUY
            if "BUY" in signal:

                if rsi <= 30:
                    score += 25

                elif rsi <= 40:
                    score += 15

            # SELL
            elif "SELL" in signal:

                if rsi >= 70:
                    score += 25

                elif rsi >= 60:
                    score += 15

        # ==================================================
        # EMA SCORE
        # ==================================================

        bullish_signals = ["LONG", "BULLISH"]
        bearish_signals = ["SHORT", "BEARISH"]

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
        # FUNDING SCORE
        # ==================================================

        if "BUY" in signal and funding < 0:
            score += 15

        elif "SELL" in signal and funding > 0:
            score += 15

        # ==================================================
        # VOLATILITY SCORE
        # ==================================================

        if volatility:

            if volatility["score"] >= 60:
                score += 20

            elif volatility["score"] >= 30:
                score += 10

        # ==================================================
        # MOVEMENT SCORE
        # ==================================================

        if movement:
            score += 15

        # ==================================================
        # LIMITAR A 100
        # ==================================================

        if score > 100:
            score = 100

        # ==================================================
        # CLASIFICACIÓN
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
        print(f"❌ Error confidence engine: {e}")

        return {
            "score": 0,
            "level": "LOW"
        }