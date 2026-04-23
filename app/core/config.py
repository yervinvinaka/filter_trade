import os
from dotenv import load_dotenv

# 🔥 Cargar .env
load_dotenv()


class Settings:
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_SECRET = os.getenv("BINANCE_SECRET")

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    WATCHLIST = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "LINKUSDT"]

    LOOP_INTERVAL = 60
    LOG_LEVEL = "INFO"


settings = Settings()