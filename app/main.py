import time
import logging

from app.services.market_service import MarketPosition

from app.services.strategy_service import (
    process_market_data
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

                # 🔥 Procesar estrategia
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

                # 🔥 CORRECCIÓN DEL ERROR
                rsi_value = round(rsi, 2) if rsi else 0

                # 🔹 LOG GENERAL
                logging.info(
                    f"{symbol} | "
                    f"RSI: {rsi_value} | "
                    f"EMA: {ema_signal} | "
                    f"Funding: {funding:.6f} | "
                    f"OI: {oi:.2f}"
                )

                # 🔥 EVITAR SPAM
                if signal and last_signals.get(symbol) != signal:

                    last_signals[symbol] = signal

                    # 🔹 Emojis dinámicos
                    emoji = "🟢"

                    if "SELL" in signal:
                        emoji = "🔴"

                    # 🔥 Mensaje principal
                    message = (
                        f"{emoji} SIGNAL ALERT\n\n"
                        f"📊 Symbol: {symbol}\n"
                        f"📈 Signal: {signal}\n"
                        f"📉 RSI: {rsi_value}\n"
                        f"📊 EMA Trend: {ema_signal}\n"
                        f"💰 Funding: {funding:.6f}\n"
                        f"📦 OI: {oi:.2f}"
                    )

                    # 🔥 Movimiento fuerte
                    if movement:
                        message += (
                            f"\n\n"
                            f"🚨 {movement['type']} DETECTED\n"
                            f"⚡ Change: {movement['change_pct']}%"
                        )

                    logging.info(f"📩 Enviando alerta: {symbol}")

                    send_alert(message)

                else:
                    logging.info(f"⏸️ Sin nueva señal en {symbol}")

            except Exception as e:
                logging.error(f"❌ Error procesando {symbol}: {e}")

        # 🔹 Espera entre ciclos
        time.sleep(60)


# 🔥 ENTRYPOINT
if __name__ == "__main__":
    run_bot()