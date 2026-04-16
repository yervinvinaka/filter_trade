# app/db/crud.py

from sqlalchemy.orm import Session
from app.db.models import Signal

def create_signal(db: Session, symbol: str, signal_type: str, price: float, rsi: float):
    db_signal = Signal(
        symbol=symbol,
        signal_type=signal_type,
        price=price,
        rsi=rsi
    )
    db.add(db_signal)
    db.commit()
    db.refresh(db_signal)
    return db_signal


def get_signals(db: Session, limit: int = 100):
    return db.query(Signal).order_by(Signal.timestamp.desc()).limit(limit).all()