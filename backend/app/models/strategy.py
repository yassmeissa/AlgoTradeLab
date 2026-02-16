"""Strategy model"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Strategy(Base):
    """Strategy model"""
    
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    strategy_type = Column(String(50), nullable=False)  # e.g., "moving_average_crossover", "rsi", "macd"
    parameters = Column(Text)  # JSON string of strategy parameters
    symbol = Column(String(20), nullable=False)  # e.g., "AAPL", "BTC/USD"
    initial_capital = Column(Float, default=10000.0)
    is_active = Column(Boolean, default=True)
    use_ml = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="strategies")
    backtest_results = relationship("BacktestResult", back_populates="strategy", cascade="all, delete-orphan")
