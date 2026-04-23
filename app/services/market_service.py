import requests


class MarketPosition:
    def __init__(self):
        self.last_data = None

    def fetch_data(self, symbol="BTCUSDT"):
        try:
            # 🔹 Open Interest
            oi_url = f"https://fapi.binance.com/fapi/v1/openInterest?symbol={symbol}"
            oi_data = requests.get(oi_url).json()
            open_interest = float(oi_data["openInterest"])

            # 🔹 Funding Rate
            funding_url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
            funding_data = requests.get(funding_url).json()
            funding_rate = float(funding_data["lastFundingRate"])

            # 🔹 Velas 4H (para RSI y movimientos)
            klines_url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=4h&limit=100"
            klines = requests.get(klines_url).json()

            closes = [float(k[4]) for k in klines]

            self.last_data = {
                "open_interest": open_interest,
                "funding_rate": funding_rate,
                "closes": closes,
                "klines": klines
            }

            return self.last_data

        except Exception as e:
            print(f"Error obteniendo market data: {e}")
            return None