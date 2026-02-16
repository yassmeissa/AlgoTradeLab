"""Backtest Result model"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class BacktestResult(Base):
    """Backtest Result model"""
    
    __tablename__ = "backtest_results"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Performance metrics
    total_return = Column(Float)  # ROI percentage
    roi = Column(Float)  # Return on Investment
    sharpe_ratio = Column(Float)
    max_drawdown = Column(Float)
    win_rate = Column(Float)  # Percentage of winning trades
    profit_factor = Column(Float)  # Total profit / Total loss
    
    # Trade statistics
    total_trades = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    average_trade = Column(Float)
    best_trade = Column(Float)
    worst_trade = Column(Float)
    
    # Additional data
    status = Column(String(50), default="completed")  # completed, running, failed
    trades = Column(JSON)  # List of trades executed
    equity_curve = Column(JSON)  # Equity over time
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    strategy = relationship("Strategy", back_populates="backtest_results")
