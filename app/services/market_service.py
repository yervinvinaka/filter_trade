import requests


BINANCE_FUTURES_URL = "https://fapi.binance.com"


class MarketPosition:
    def __init__(self):
        self.last_data = None

    def fetch_data(self, symbol="BTCUSDT"):
        try:
            # 🔹 Open Interest
            oi_url = f"{BINANCE_FUTURES_URL}/fapi/v1/openInterest?symbol={symbol}"
            oi_data = requests.get(oi_url, timeout=10).json()
            open_interest = float(oi_data["openInterest"])

            # 🔹 Funding Rate
            funding_url = f"{BINANCE_FUTURES_URL}/fapi/v1/premiumIndex?symbol={symbol}"
            funding_data = requests.get(funding_url, timeout=10).json()
            funding_rate = float(funding_data["lastFundingRate"])

            # 🔹 Velas 4H
            klines_url = f"{BINANCE_FUTURES_URL}/fapi/v1/klines?symbol={symbol}&interval=4h&limit=100"
            klines = requests.get(klines_url, timeout=10).json()

            closes = [float(k[4]) for k in klines]

            self.last_data = {
                "open_interest": open_interest,
                "funding_rate": funding_rate,
                "closes": closes,
                "klines": klines
            }

            return self.last_data

        except Exception as e:
            print(f"❌ Error obteniendo market data: {e}")
            return None


# 🔹 EMA MANUAL
def calculate_ema(prices, period):
    try:
        if len(prices) < period:
            return []

        ema_values = []

        sma = sum(prices[:period]) / period
        ema_values.append(sma)

        multiplier = 2 / (period + 1)

        for price in prices[period:]:
            ema = (price - ema_values[-1]) * multiplier + ema_values[-1]
            ema_values.append(ema)

        return ema_values

    except Exception as e:
        print(f"❌ Error calculando EMA: {e}")
        return []


# 🔹 DETECCIÓN DE CRUCE EMA
def get_ema_signal(prices):
    try:
        ema_fast = calculate_ema(prices, 9)
        ema_slow = calculate_ema(prices, 21)

        if len(ema_fast) < 2 or len(ema_slow) < 2:
            return "NEUTRAL"

        fast_now = ema_fast[-1]
        fast_prev = ema_fast[-2]

        slow_now = ema_slow[-1]
        slow_prev = ema_slow[-2]

        # 🔥 Golden Cross
        if fast_prev < slow_prev and fast_now > slow_now:
            return "LONG"

        # 🔥 Death Cross
        elif fast_prev > slow_prev and fast_now < slow_now:
            return "SHORT"

        # 🔹 Tendencia actual
        elif fast_now > slow_now:
            return "BULLISH"

        elif fast_now < slow_now:
            return "BEARISH"

        return "NEUTRAL"

    except Exception as e:
        print(f"❌ Error obteniendo señal EMA: {e}")
        return "NEUTRAL"