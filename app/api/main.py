from fastapi import FastAPI
from app.db.database import init_db, get_connection

app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}


@app.get("/signals")
def get_signals():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM signals ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    signals = [
        {
            "id": row[0],
            "symbol": row[1],
            "signal": row[2],
            "rsi": row[3],
            "timestamp": row[4],
        }
        for row in rows
    ]

    return {"signals": signals}