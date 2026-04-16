from fastapi import FastAPI
import threading

from app.db.database import init_db, get_connection
from app.main import run_bot  # 👈 importa tu bot

app = FastAPI()


@app.on_event("startup")
def startup():
    # Inicializa DB
    init_db()

    # Arranca el bot en background
    def bot_runner():
        print("🤖 Bot iniciado desde API...")
        run_bot()

    thread = threading.Thread(target=bot_runner, daemon=True)
    thread.start()


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