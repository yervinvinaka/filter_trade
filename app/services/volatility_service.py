def analyze_volatility(klines, open_interest=None):
    try:

        if len(klines) < 5:
            return None

        last = klines[-1]
        previous = klines[-2]

        # 🔹 Datos vela actual
        open_price = float(last[1])
        close_price = float(last[4])
        volume = float(last[5])

        # 🔹 Datos vela anterior
        prev_volume = float(previous[5])

        # 🔥 Cambio %
        change_pct = (
            (close_price - open_price) / open_price
        ) * 100

        # 🔥 Cambio volumen
        volume_change = 0

        if prev_volume > 0:
            volume_change = (
                (volume - prev_volume) / prev_volume
            ) * 100

        # 🔥 Score de volatilidad
        score = 0

        if abs(change_pct) >= 2:
            score += 30

        if abs(change_pct) >= 4:
            score += 30

        if volume_change >= 50:
            score += 20

        if volume_change >= 100:
            score += 20

        # 🔥 Clasificación
        event = None

        if change_pct >= 3:
            event = "PUMP"

        elif change_pct <= -3:
            event = "DUMP"

        if score >= 60:
            strength = "HIGH"

        elif score >= 30:
            strength = "MEDIUM"

        else:
            strength = "LOW"

        return {
            "event": event,
            "strength": strength,
            "score": score,
            "change_pct": round(change_pct, 2),
            "volume_change": round(volume_change, 2)
        }

    except Exception as e:
        print(f"❌ Error volatility engine: {e}")
        return None