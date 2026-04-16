import pandas as pd
import pandas_ta as ta

def calculate_rsi(klines):
    df = pd.DataFrame(klines, columns=[
        "time","open","high","low","close","volume",
        "close_time","qav","trades","tbbav","tbqav","ignore"
    ])

    df["close"] = df["close"].astype(float)

    df["rsi"] = ta.rsi(df["close"], length=14)

    return df