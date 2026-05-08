def interpret_signal(
    signal,
    rsi,
    ema_signal,
    confidence=None,
    movement=None,
    volatility=None
):

    try:

        interpretation = []

        # ==================================================
        # BUY SIGNALS
        # ==================================================

        if signal and "BUY" in signal:

            interpretation.append(
                "📈 El mercado muestra "
                "posibles señales alcistas."
            )

            if rsi <= 30:

                interpretation.append(
                    "🔥 RSI en sobreventa, "
                    "posible rebote fuerte."
                )

            elif rsi <= 40:

                interpretation.append(
                    "⚠️ RSI recuperándose "
                    "desde zona débil."
                )

        # ==================================================
        # SELL SIGNALS
        # ==================================================

        elif signal and "SELL" in signal:

            interpretation.append(
                "📉 El mercado muestra "
                "debilidad bajista."
            )

            if rsi >= 70:

                interpretation.append(
                    "🔥 RSI en sobrecompra, "
                    "riesgo de caída fuerte."
                )

            elif rsi >= 60:

                interpretation.append(
                    "⚠️ Momentum alcista "
                    "comienza a debilitarse."
                )

        # ==================================================
        # EMA TREND
        # ==================================================

        if ema_signal == "BULLISH":

            interpretation.append(
                "🟢 Tendencia EMA "
                "mantiene estructura alcista."
            )

        elif ema_signal == "BEARISH":

            interpretation.append(
                "🔴 EMAs muestran "
                "presión bajista."
            )

        # ==================================================
        # CONFIDENCE
        # ==================================================

        if confidence:

            if confidence["level"] == "HIGH":

                interpretation.append(
                    "🚀 Setup con alta "
                    "probabilidad."
                )

            elif confidence["level"] == "MEDIUM":

                interpretation.append(
                    "⚠️ Setup moderado, "
                    "requiere confirmación."
                )

            else:

                interpretation.append(
                    "❌ Señal débil "
                    "o poco confirmada."
                )

        # ==================================================
        # VOLATILITY
        # ==================================================

        if volatility:

            if volatility["score"] >= 70:

                interpretation.append(
                    "🔥 Alta volatilidad "
                    "detectada."
                )

        # ==================================================
        # MOVEMENT
        # ==================================================

        if movement:

            interpretation.append(
                f"🚨 Movimiento "
                f"{movement['type']} "
                f"detectado recientemente."
            )

        # ==================================================
        # RESULT
        # ==================================================

        return "\n".join(interpretation)

    except Exception as e:

        print(
            f"❌ Error interpreter: {e}"
        )

        return (
            "⚠️ No se pudo interpretar "
            "la señal."
        )