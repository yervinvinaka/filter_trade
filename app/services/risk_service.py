def calculate_atr(klines, period=14):

    try:

        if len(klines) < period + 1:
            return None

        true_ranges = []

        for i in range(1, len(klines)):

            current = klines[i]
            previous = klines[i - 1]

            high = float(current[2])
            low = float(current[3])

            prev_close = float(previous[4])

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )

            true_ranges.append(tr)

        atr = sum(true_ranges[-period:]) / period

        return atr

    except Exception as e:
        print(f"❌ Error calculando ATR: {e}")
        return None


def calculate_trade_levels(signal, current_price, atr):

    try:

        if not signal or not atr:
            return None

        entry = current_price

        # ==================================================
        # BUY SETUP
        # ==================================================

        if "BUY" in signal:

            stop_loss = entry - (atr * 1.5)

            take_profit = entry + (atr * 3)

        # ==================================================
        # SELL SETUP
        # ==================================================

        elif "SELL" in signal:

            stop_loss = entry + (atr * 1.5)

            take_profit = entry - (atr * 3)

        else:
            return None

        # 🔥 Risk Reward
        risk = abs(entry - stop_loss)

        reward = abs(take_profit - entry)

        rr = reward / risk if risk > 0 else 0

        return {
            "entry": round(entry, 2),
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "risk_reward": round(rr, 2),
            "atr": round(atr, 2)
        }

    except Exception as e:
        print(f"❌ Error trade levels: {e}")
        return None