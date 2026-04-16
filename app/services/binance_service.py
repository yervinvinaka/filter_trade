import requests

BASE_URL = "https://api.binance.com/api/v3/klines"


def get_klines(symbol, interval="1m", limit=100):
    """
    Obtiene velas (klines) desde Binance
    """

    try:
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"{symbol} | Error API Binance: {response.status_code}")
            return None

        return response.json()

    except Exception as e:
        print(f"{symbol} | Error conexión Binance: {str(e)}")
        return None