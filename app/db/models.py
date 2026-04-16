# app/db/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.database import Base

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    signal_type = Column(String)  # BUY_WEAK, SELL_STRONG, etc.
    price = Column(Float)
    rsi = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)