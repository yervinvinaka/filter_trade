# ==================================================
# 🔥 MARKET STRUCTURE ENGINE
# ==================================================

def analyze_market_structure(klines):

    try:

        if len(klines) < 10:
            return None

        highs = [
            float(k[2])
            for k in klines[-10:]
        ]

        lows = [
            float(k[3])
            for k in klines[-10:]
        ]

        # ==================================================
        # 🔥 RECENT STRUCTURE
        # ==================================================

        recent_high_1 = highs[-1]
        recent_high_2 = highs[-3]

        recent_low_1 = lows[-1]
        recent_low_2 = lows[-3]

        # ==================================================
        # 🔥 BULLISH STRUCTURE
        # ==================================================

        if (
            recent_high_1 > recent_high_2
            and recent_low_1 > recent_low_2
        ):

            return {
                "structure": "BULLISH",
                "trend": "HIGHER_HIGHS"
            }

        # ==================================================
        # 🔥 BEARISH STRUCTURE
        # ==================================================

        elif (
            recent_high_1 < recent_high_2
            and recent_low_1 < recent_low_2
        ):

            return {
                "structure": "BEARISH",
                "trend": "LOWER_LOWS"
            }

        # ==================================================
        # 🔥 SIDEWAYS
        # ==================================================

        return {
            "structure": "RANGING",
            "trend": "SIDEWAYS"
        }

    except Exception as e:

        print(
            f"❌ Market structure error: {e}"
        )

        return None