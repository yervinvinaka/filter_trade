import sqlite3
from datetime import datetime
import os

DB_NAME = "data/signals.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        signal TEXT,
        rsi REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_signal(symbol, signal, rsi):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Evitar duplicados consecutivos
    cursor.execute("""
    SELECT signal FROM signals
    WHERE symbol = ?
    ORDER BY id DESC LIMIT 1
    """, (symbol,))
    
    last = cursor.fetchone()

    if last and last[0] == signal:
        conn.close()
        return

    cursor.execute("""
    INSERT INTO signals (symbol, signal, rsi, timestamp)
    VALUES (?, ?, ?, ?)
    """, (symbol, signal, rsi, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()