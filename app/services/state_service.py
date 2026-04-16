last_signals = {}

def should_send_signal(symbol, new_signal):
    """
    Evita enviar señales repetidas (anti-spam)
    """

    last_signal = last_signals.get(symbol)

    # Si es la misma señal que antes → NO enviar
    if last_signal == new_signal:
        return False

    # Guardar nueva señal
    last_signals[symbol] = new_signal
    return True