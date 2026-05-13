import numpy as np


# ==================================================
# 🔥 RSI MOMENTUM
# ==================================================

def validate_rsi_momentum(closes):

    try:

        if len(closes) < 20:
            return False

        recent = closes[-5:]

        momentum = recent[-1] - recent[0]

        return momentum > 0

    except Exception as e:

        print(f"❌ RSI momentum error: {e}")

        return False


# ==================================================
# 🔥 CANDLE STRENGTH
# ==================================================

def validate_candle_strength(klines):

    try:

        last = klines[-1]

        open_price = float(last[1])

        close_price = float(last[4])

        high = float(last[2])

        low = float(last[3])

        body = abs(close_price - open_price)

        range_total = high - low

        if range_total == 0:
            return False

        strength = body / range_total

        return strength >= 0.5

    except Exception as e:

        print(f"❌ Candle strength error: {e}")

        return False


# ==================================================
# 🔥 VOLUME CONFIRMATION
# ==================================================

def validate_volume(klines):

    try:

        volumes = [
            float(k[5])
            for k in klines[-10:]
        ]

        avg_volume = np.mean(volumes[:-1])

        current_volume = volumes[-1]

        return current_volume > avg_volume

    except Exception as e:

        print(f"❌ Volume validation error: {e}")

        return False


# ==================================================
# 🔥 MAIN CONFIRMATION
# ==================================================

def confirm_trade(closes, klines):

    confirmations = 0

    if validate_rsi_momentum(closes):
        confirmations += 1

    if validate_candle_strength(klines):
        confirmations += 1

    if validate_volume(klines):
        confirmations += 1

    return {
        "score": confirmations,
        "valid": confirmations >= 2
    }