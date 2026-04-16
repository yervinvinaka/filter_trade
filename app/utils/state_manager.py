last_signals = {}

def should_send_alert(symbol, new_signal):
    global last_signals

    # Si nunca se envió señal → enviar
    if symbol not in last_signals:
        last_signals[symbol] = new_signal
        return True

    # Si la señal cambió → enviar
    if last_signals[symbol] != new_signal:
        last_signals[symbol] = new_signal
        return True

    # Si es la misma señal → NO enviar
    return False