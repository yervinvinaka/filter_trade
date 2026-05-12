import requests


class MarketPosition:

    def __init__(self):

        self.last_data = None

    # ==================================================
    # 🔥 FETCH MARKET DATA
    # ==================================================

    def fetch_data(self, symbol="BTCUSDT"):

        try:

            # ==================================================
            # 🔹 OPEN INTEREST
            # ==================================================

            oi_url = (
                f"https://fapi.binance.com/"
                f"fapi/v1/openInterest?symbol={symbol}"
            )

            oi_data = requests.get(
                oi_url,
                timeout=10
            ).json()

            # 🔥 VALIDAR RESPUESTA

            if "openInterest" not in oi_data:

                print(
                    f"⚠️ Binance OI error: "
                    f"{oi_data}"
                )

                return None

            open_interest = float(
                oi_data["openInterest"]
            )

            # ==================================================
            # 🔹 FUNDING RATE
            # ==================================================

            funding_url = (
                f"https://fapi.binance.com/"
                f"fapi/v1/premiumIndex?symbol={symbol}"
            )

            funding_data = requests.get(
                funding_url,
                timeout=10
            ).json()

            # 🔥 VALIDAR RESPUESTA

            if "lastFundingRate" not in funding_data:

                print(
                    f"⚠️ Binance funding error: "
                    f"{funding_data}"
                )

                return None

            funding_rate = float(
                funding_data["lastFundingRate"]
            )

            # ==================================================
            # 🔹 KLINES
            # ==================================================

            klines_url = (
                f"https://api.binance.com/"
                f"api/v3/klines?"
                f"symbol={symbol}"
                f"&interval=4h"
                f"&limit=100"
            )

            klines = requests.get(
                klines_url,
                timeout=10
            ).json()

            closes = [
                float(k[4])
                for k in klines
            ]

            # ==================================================
            # 🔹 SAVE DATA
            # ==================================================

            self.last_data = {
                "open_interest": open_interest,
                "funding_rate": funding_rate,
                "closes": closes,
                "klines": klines
            }

            return self.last_data

        except Exception as e:

            print(
                f"❌ Error obteniendo market data: {e}"
            )

            return None


# ==================================================
# 🔥 EMA CALCULATION
# ==================================================

def calculate_ema(closes, period):

    multiplier = 2 / (period + 1)

    ema = closes[0]

    for price in closes[1:]:

        ema = (
            (price - ema)
            * multiplier
        ) + ema

    return ema


# ==================================================
# 🔥 EMA SIGNAL
# ==================================================

def get_ema_signal(closes):

    try:

        ema_fast = calculate_ema(
            closes,
            9
        )

        ema_slow = calculate_ema(
            closes,
            21
        )

        if ema_fast > ema_slow:
            return "BULLISH"

        elif ema_fast < ema_slow:
            return "BEARISH"

        return "NEUTRAL"

    except Exception as e:

        print(
            f"❌ Error EMA signal: {e}"
        )

        return "NEUTRAL"