import time
import logging

from app.services.market_service import MarketPosition
from app.alerts.alert_service import send_alert

print("🔥 BOT ARRANCANDO EN RAILWAY")

# 🔥 Configuración de logs más limpia
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "LINKUSDT"]

# 🔥 Para evitar spam (memoria de última señal)
last_signals = {}


def run_bot():
    logging.info("🚀 Bot iniciado...")

    market = MarketPosition()

    while True:
        logging.info("📊 Analizando mercado...")

        for symbol in symbols:
            data = market.fetch_data(symbol)

            if not data:
                continue

            oi = data["open_interest"]
            funding = data["funding_rate"]

            log_msg = f"{symbol} | OI: {oi:.2f} | Funding: {funding:.6f}"
            logging.info(log_msg)

            # 🔥 Detectar tipo de señal
            signal = None

            if funding > 0.0001:
                signal = "LONG"

            elif funding < -0.0001:
                signal = "SHORT"

            # 🔥 Evitar repetir la misma señal
            if signal and last_signals.get(symbol) != signal:
                last_signals[symbol] = signal

                if signal == "LONG":
                    message = (
                        f"🚀 POSIBLE LONG\n"
                        f"{symbol}\n"
                        f"Funding: {funding:.6f}\n"
                        f"OI: {oi:.2f}"
                    )

                else:
                    message = (
                        f"🔻 POSIBLE SHORT\n"
                        f"{symbol}\n"
                        f"Funding: {funding:.6f}\n"
                        f"OI: {oi:.2f}"
                    )

                logging.info(f"📩 Enviando alerta {signal}: {symbol}")
                send_alert(message)

            else:
                logging.info(f"Sin cambio de señal en {symbol}")

        time.sleep(60)


# 🔥 ENTRYPOINT
if __name__ == "__main__":
    run_bot()