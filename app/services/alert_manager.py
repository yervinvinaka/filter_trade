# app/main.py

import time

from config import WATCHLIST
from app.services.binance_service import get_klines
from app.services.strategy_service import evaluate_market
from app.services.social_service import get_social_sentiment
from app.alerts.alert_service import send_alert


def run_bot():
    try:
        while True:
            print("\n📊 Analizando mercado...\n")

            for symbol in WATCHLIST:

                # 📈 Datos de mercado
                klines = get_klines(symbol)

                # 🧠 Estrategia (RSI)
                market_data = evaluate_market(klines)
                rsi = market_data["rsi"]
                signal = market_data["signal"]

                # 🌐 Social
                mentions = get_social_sentiment(symbol)

                print(f"{symbol} | RSI: {rsi:.2f} | Señal: {signal} | Menciones: {mentions}")

                # 🎯 SCORE INTELIGENTE
                score = 0

                if signal == "LONG":
                    score += 1
                elif signal == "SHORT":
                    score += 1

                if mentions >= 5:
                    score += 1

                # 🚨 ALERTA SOLO SI ES FUERTE
                if score >= 2:
                    message = (
                        f"🚀 {symbol}\n"
                        f"Señal: {signal}\n"
                        f"RSI: {rsi:.2f}\n"
                        f"Menciones: {mentions}\n"
                        f"Score: {score}/2"
                    )

                    send_alert(message)

            print("\n------ esperando actualización ------\n")
            time.sleep(60)

    except KeyboardInterrupt:
        print("\n🛑 Sistema detenido manualmente")


if __name__ == "__main__":
    run_bot()