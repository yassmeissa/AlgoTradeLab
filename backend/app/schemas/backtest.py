"""Backtest schemas"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class BacktestRequest(BaseModel):
    """Backtest request schema"""
    strategy_id: int
    start_date: datetime
    end_date: datetime


class TradeInfo(BaseModel):
    """Trade information schema"""
    entry_date: datetime
    exit_date: Optional[datetime]
    entry_price: float
    exit_price: Optional[float]
    quantity: int
    side: str  # "BUY" or "SELL"
    pnl: Optional[float]
    pnl_percent: Optional[float]


class BacktestResultResponse(BaseModel):
    """Backtest result response schema"""
    id: int
    strategy_id: int
    start_date: datetime
    end_date: datetime
    
    # Performance metrics
    total_return: Optional[float]
    roi: Optional[float]
    sharpe_ratio: Optional[float]
    max_drawdown: Optional[float]
    win_rate: Optional[float]
    profit_factor: Optional[float]
    
    # Trade statistics
    total_trades: Optional[int]
    winning_trades: Optional[int]
    losing_trades: Optional[int]
    average_trade: Optional[float]
    best_trade: Optional[float]
    worst_trade: Optional[float]
    
    status: str
    trades: Optional[List[Dict[str, Any]]]
    created_at: datetime
    
    class Config:
        from_attributes = True


class BacktestComparison(BaseModel):
    """Backtest comparison between classic and ML strategy"""
    classic_result: BacktestResultResponse
    ml_result: BacktestResultResponse
    performance_difference: Dict[str, float]  # Differences in key metrics
