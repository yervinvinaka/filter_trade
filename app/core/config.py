import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()


class Settings:
    # 🔐 APIs
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_SECRET = os.getenv("BINANCE_SECRET")

    # 🤖 Telegram
    TELEGRAM_TOKEN = os.getenv("8212208208:AAFMBKBrfQOoEGg8TTuSY8Wtltz85t2OVsw")
    TELEGRAM_CHAT_ID = os.getenv("1357188939")

    # 📊 Configuración del bot
    WATCHLIST = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "LINKUSDT"]

    LOOP_INTERVAL = 60  # segundos

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()