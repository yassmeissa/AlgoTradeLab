"""Data models for backtesting results"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class TradeExecuted:
    """Trade execution record"""
    entry_date: datetime
    exit_date: datetime
    entry_price: float
    exit_price: float
    quantity: int
    side: str  # BUY or SELL
    pnl: float
    pnl_percent: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class StrategyPerformance:
    """Strategy performance summary"""
    strategy_name: str
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float
    
    # Returns
    total_return: float
    roi: float
    
    # Risk metrics
    sharpe_ratio: float
    max_drawdown: float
    
    # Trade statistics
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    profit_factor: float
    average_trade: float
    best_trade: float
    worst_trade: float
    
    # Execution details
    trades: List[TradeExecuted]
    equity_curve: List[float]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = asdict(self)
        result['start_date'] = self.start_date.isoformat()
        result['end_date'] = self.end_date.isoformat()
        result['trades'] = [t.to_dict() for t in self.trades]
        return result
    
    def summary(self) -> str:
        """Get summary string"""
        return f"""
Strategy Performance Summary
=============================
Strategy: {self.strategy_name}
Period: {self.start_date.date()} to {self.end_date.date()}

Performance:
- ROI: {self.roi:.2f}%
- Total Return: ${self.total_return:,.2f}
- Sharpe Ratio: {self.sharpe_ratio:.2f}
- Max Drawdown: {self.max_drawdown:.2f}%

Trading:
- Total Trades: {self.total_trades}
- Winning Trades: {self.winning_trades}
- Losing Trades: {self.losing_trades}
- Win Rate: {self.win_rate:.2f}%
- Profit Factor: {self.profit_factor:.2f}

Trade Statistics:
- Average Trade: ${self.average_trade:,.2f}
- Best Trade: ${self.best_trade:,.2f}
- Worst Trade: ${self.worst_trade:,.2f}

Capital:
- Initial: ${self.initial_capital:,.2f}
- Final: ${self.final_capital:,.2f}
"""
