import time
import logging

from app.services.market_service import MarketPosition

logging.basicConfig(level=logging.INFO)

def run_bot():
    logging.info("🚀 Bot iniciado...")

    market = MarketPosition()

    while True:
        logging.info("📊 Analizando mercado...")

        symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "LINKUSDT"]

        for symbol in symbols:
            data = market.fetch_data(symbol)

            if data:
                logging.info(
                    f"{symbol} | OI: {data['open_interest']} | Funding: {data['funding_rate']}"
                )

        time.sleep(60)