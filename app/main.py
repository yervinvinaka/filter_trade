import time
import logging

from app.services.binance_service import get_klines
from app.services.strategy_service import calculate_rsi, get_signal
from app.alerts.alert_service import send_alert

from app.db.database import init_db, save_signal
from app.services.state_service import should_send_signal

# 🔧 Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# 📊 Lista de criptos
WATCHLIST = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "LINKUSDT"]


def run_bot():
    logging.info("🚀 Bot iniciado...")

    # 🧱 Inicializar base de datos
    init_db()

    while True:
        logging.info("📊 Analizando mercado...")

        for symbol in WATCHLIST:
            try:
                # 📡 Obtener datos
                klines = get_klines(symbol)

                if not klines or len(klines) < 15:
                    logging.warning(f"{symbol} | Datos insuficientes")
                    continue

                # 📉 Precios de cierre
                closes = [float(k[4]) for k in klines]

                # 📊 RSI
                rsi = calculate_rsi(closes)
                logging.info(f"{symbol} | RSI: {round(rsi, 2)}")

                # 🚨 Señal
                signal = get_signal(rsi)

                if signal:
                    logging.info(f"{symbol} | Señal detectada: {signal}")

                    # 🧠 Anti-spam
                    if should_send_signal(symbol, signal):

                        # 💾 Guardar en DB
                        save_signal(symbol, signal, rsi)

                        # 📩 Mensaje
                        message = f"""
📊 {symbol}
🚨 Señal: {signal}
📉 RSI: {round(rsi, 2)}
"""

                        # 📲 Enviar a Telegram
                        send_alert(message)

                    else:
                        logging.info(f"{symbol} | Señal repetida (omitida)")

            except Exception as e:
                logging.error(f"{symbol} | Error: {str(e)}")

        # ⏱️ Delay
        time.sleep(60)


if __name__ == "__main__":
    run_bot()