import os

class Settings:
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_SECRET = os.getenv("BINANCE_SECRET")

    TELEGRAM_TOKEN = os.getenv("8635347002:AAHYH1Olc8BQFUPZOVdCPtaGMqpjpPmZWUk")
    TELEGRAM_CHAT_ID = os.getenv("1357188939")

    WATCHLIST = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "LINKUSDT"]

    LOOP_INTERVAL = 60  # segundos

    LOG_LEVEL = "INFO"

settings = Settings()