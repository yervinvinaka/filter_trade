import time
import logging

from app.services.market_service import MarketPosition

from app.services.strategy_service import (
    process_market_data
)

from app.services.volatility_service import (
    analyze_volatility
)

from app.alerts.alert_service import send_alert


print("🔥 BOT ARRANCANDO EN RAILWAY")


# 🔹 Configuración logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "LINKUSDT"
]


# 🔥 Evitar spam
last_signals = {}

# 🔥 Evitar spam volatilidad
last_volatility_alert = {}


def run_bot():
    logging.info("🚀 Bot iniciado...")

    market = MarketPosition()

    while True:
        logging.info("📊 Analizando mercado...")

        for symbol in symbols:

            try:
                data = market.fetch_data(symbol)

                if not data:
                    continue

                oi = data["open_interest"]
                funding = data["funding_rate"]
                closes = data["closes"]
                klines = data["klines"]

                # 🔥 Procesar estrategia principal
                result = process_market_data(
                    symbol,
                    closes,
                    klines
                )

                if not result:
                    continue

                signal = result["signal"]
                rsi = result["rsi"]
                ema_signal = result["ema_signal"]
                movement = result["movement"]

                # 🔥 Volatility Engine
                volatility = analyze_volatility(
                    klines,
                    oi
                )

                # 🔹 RSI seguro
                rsi_value = round(rsi, 2) if rsi else 0

                # 🔹 LOG GENERAL
                logging.info(
                    f"{symbol} | "
                    f"RSI: {rsi_value} | "
                    f"EMA: {ema_signal} | "
                    f"Funding: {funding:.6f} | "
                    f"OI: {oi:.2f}"
                )

                # ==================================================
                # 🔥 ALERTAS DE SIGNAL
                # ==================================================

                if signal and last_signals.get(symbol) != signal:

                    last_signals[symbol] = signal

                    emoji = "🟢"

                    if "SELL" in signal:
                        emoji = "🔴"

                    message = (
                        f"{emoji} SIGNAL ALERT\n\n"
                        f"📊 Symbol: {symbol}\n"
                        f"📈 Signal: {signal}\n"
                        f"📉 RSI: {rsi_value}\n"
                        f"📊 EMA Trend: {ema_signal}\n"
                        f"💰 Funding: {funding:.6f}\n"
                        f"📦 OI: {oi:.2f}"
                    )

                    # 🔥 Movimiento detectado
                    if movement:
                        message += (
                            f"\n\n"
                            f"🚨 {movement['type']} DETECTED\n"
                            f"⚡ Change: {movement['change_pct']}%"
                        )

                    logging.info(f"📩 Enviando SIGNAL ALERT: {symbol}")

                    send_alert(message)

                else:
                    logging.info(f"⏸️ Sin nueva señal en {symbol}")

                # ==================================================
                # 🔥 ALERTAS DE VOLATILIDAD
                # ==================================================

                if (
                    volatility
                    and volatility["score"] >= 60
                ):

                    volatility_key = (
                        f"{symbol}_{volatility['event']}"
                    )

                    # 🔥 Evitar spam
                    if (
                        last_volatility_alert.get(symbol)
                        != volatility_key
                    ):

                        last_volatility_alert[symbol] = volatility_key

                        volatility_msg = (
                            f"⚠️ HIGH VOLATILITY DETECTED\n\n"
                            f"📊 Symbol: {symbol}\n"
                            f"🔥 Event: {volatility['event']}\n"
                            f"⚡ Strength: {volatility['strength']}\n"
                            f"📈 Price Change: {volatility['change_pct']}%\n"
                            f"📦 Volume Change: {volatility['volume_change']}%\n"
                            f"🎯 Score: {volatility['score']}"
                        )

                        logging.info(
                            f"🚨 Volatility alert: {symbol}"
                        )

                        send_alert(volatility_msg)

            except Exception as e:
                logging.error(
                    f"❌ Error procesando {symbol}: {e}"
                )

        # 🔹 Espera entre ciclos
        time.sleep(60)


# 🔥 ENTRYPOINT
if __name__ == "__main__":
    run_bot()