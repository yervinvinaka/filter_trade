from binance import ThreadedWebsocketManager


def start_trade_socket(callback):
    twm = ThreadedWebsocketManager()
    twm.start()

    def safe_callback(msg):
        try:
            callback(msg)
        except Exception as e:
            # 🔥 Ignorar errores cuando el socket ya murió
            if "closed" not in str(e):
                print(f"Error en callback: {e}")

    twm.start_trade_socket(
        callback=safe_callback,
        symbol='btcusdt'
    )

    return twm