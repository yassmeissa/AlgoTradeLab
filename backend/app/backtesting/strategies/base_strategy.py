"""Base strategy class"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd
from dataclasses import dataclass


@dataclass
class Trade:
    """Trade data class"""
    entry_date: pd.Timestamp
    entry_price: float
    exit_date: pd.Timestamp
    exit_price: float
    quantity: int
    side: str  # "BUY" or "SELL"
    pnl: float
    pnl_percent: float


class BaseStrategy(ABC):
    """Base class for all trading strategies"""
    
    def __init__(self, name: str, parameters: Dict[str, Any]):
        """Initialize strategy"""
        self.name = name
        self.parameters = parameters
        self.signals = []
        self.trades = []
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals. Must return DataFrame with 'signal' column.
        Signal values:
        - 1 = BUY signal
        - -1 = SELL signal
        - 0 = HOLD (no action)
        """
        pass
    
    def _validate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean signals DataFrame"""
        if "signal" not in data.columns:
            raise ValueError("signals DataFrame must contain 'signal' column")
        
        # Ensure signal values are in {-1, 0, 1}
        data["signal"] = data["signal"].fillna(0).astype(int)
        valid_signals = data["signal"].isin([-1, 0, 1])
        if not valid_signals.all():
            raise ValueError("Signal values must be -1 (SELL), 0 (HOLD), or 1 (BUY)")
        
        return data
    
    def get_trades(self) -> List[Trade]:
        """Get all executed trades"""
        return self.trades
    
    def _add_trade(self, entry_date: pd.Timestamp, entry_price: float, 
                   exit_date: pd.Timestamp, exit_price: float, 
                   quantity: int, side: str):
        """Add a trade to the trades list"""
        pnl = (exit_price - entry_price) * quantity if side == "BUY" else (entry_price - exit_price) * quantity
        pnl_percent = ((exit_price - entry_price) / entry_price * 100) if side == "BUY" else ((entry_price - exit_price) / entry_price * 100)
        
        trade = Trade(
            entry_date=entry_date,
            entry_price=entry_price,
            exit_date=exit_date,
            exit_price=exit_price,
            quantity=quantity,
            side=side,
            pnl=pnl,
            pnl_percent=pnl_percent
        )
        self.trades.append(trade)
        return trade
