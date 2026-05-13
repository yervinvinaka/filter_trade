import requests


class MarketPosition:

    def __init__(self):

        self.last_data = None

    # ==================================================
    # 🔥 FETCH MARKET DATA
    # ==================================================

    def fetch_data(
        self,
        symbol="BTCUSDT"
    ):

        try:

            # ==================================================
            # 🔹 DEFAULT VALUES
            # ==================================================

            open_interest = 0
            funding_rate = 0

            # ==================================================
            # 🔹 OPEN INTEREST
            # ==================================================

            try:

                oi_url = (
                    "https://fapi.binance.com/"
                    "fapi/v1/openInterest"
                    f"?symbol={symbol}"
                )

                oi_response = requests.get(
                    oi_url,
                    timeout=10
                )

                oi_data = oi_response.json()

                if (
                    isinstance(oi_data, dict)
                    and "openInterest" in oi_data
                ):

                    open_interest = float(
                        oi_data["openInterest"]
                    )

                else:

                    print(
                        f"⚠️ Binance OI error: "
                        f"{oi_data}"
                    )

            except Exception as e:

                print(
                    f"⚠️ OI fetch failed: {e}"
                )

            # ==================================================
            # 🔹 FUNDING RATE
            # ==================================================

            try:

                funding_url = (
                    "https://fapi.binance.com/"
                    "fapi/v1/premiumIndex"
                    f"?symbol={symbol}"
                )

                funding_response = requests.get(
                    funding_url,
                    timeout=10
                )

                funding_data = (
                    funding_response.json()
                )

                if (
                    isinstance(funding_data, dict)
                    and "lastFundingRate"
                    in funding_data
                ):

                    funding_rate = float(
                        funding_data[
                            "lastFundingRate"
                        ]
                    )

                else:

                    print(
                        f"⚠️ Binance Funding error: "
                        f"{funding_data}"
                    )

            except Exception as e:

                print(
                    f"⚠️ Funding fetch failed: {e}"
                )

            # ==================================================
            # 🔹 KLINES 4H
            # ==================================================

            klines_url = (
                "https://api.binance.com/"
                "api/v3/klines"
                f"?symbol={symbol}"
                "&interval=4h"
                "&limit=100"
            )

            klines_response = requests.get(
                klines_url,
                timeout=10
            )

            klines = klines_response.json()

            if not isinstance(
                klines,
                list
            ):

                print(
                    f"❌ Invalid klines: "
                    f"{klines}"
                )

                return None

            closes = [
                float(k[4])
                for k in klines
            ]

            # ==================================================
            # 🔥 FINAL DATA
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
                f"❌ Error obteniendo "
                f"market data: {e}"
            )

            return None


# ==================================================
# 🔥 EMA
# ==================================================

def calculate_ema(
    closes,
    period
):

    if len(closes) < period:
        return None

    multiplier = (
        2 / (period + 1)
    )

    ema = closes[0]

    for close in closes[1:]:

        ema = (
            (close - ema)
            * multiplier
        ) + ema

    return ema


# ==================================================
# 🔥 RSI
# ==================================================

def calculate_rsi(
    closes,
    period=14
):

    if len(closes) < period + 1:
        return None

    gains = []
    losses = []

    for i in range(
        1,
        period + 1
    ):

        delta = (
            closes[i]
            - closes[i - 1]
        )

        if delta >= 0:
            gains.append(delta)
        else:
            losses.append(abs(delta))

    avg_gain = (
        sum(gains) / period
        if gains else 0
    )

    avg_loss = (
        sum(losses) / period
        if losses else 0
    )

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss

    rsi = (
        100
        - (100 / (1 + rs))
    )

    return round(rsi, 2)

# ==================================================
# 🔥 EMA SIGNAL
# ==================================================

def get_ema_signal(closes):

    try:

        if len(closes) < 21:
            return "NEUTRAL"

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
            f"❌ EMA signal error: {e}"
        )

        return "NEUTRAL"