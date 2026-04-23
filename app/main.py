import time
import logging

from app.services.market_service import MarketPosition
from app.alerts.alert_service import send_alert

print("🔥 BOT ARRANCANDO EN RAILWAY")

logging.basicConfig(level=logging.INFO)

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "LINKUSDT"]


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

            # 🚨 ALERTAS
            if funding > 0.0001:
                send_alert(f"🚀 POSIBLE LONG\n{symbol}\nFunding: {funding:.6f}")

            elif funding < -0.0001:
                send_alert(f"🔻 POSIBLE SHORT\n{symbol}\nFunding: {funding:.6f}")

        time.sleep(60)


# 🔥 ESTO ES LO QUE TE FALTABA
if __name__ == "__main__":
    run_bot()