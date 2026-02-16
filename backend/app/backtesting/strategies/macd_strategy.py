"""MACD Strategy"""

import pandas as pd
from typing import Dict, Any
from app.backtesting.strategies.base_strategy import BaseStrategy
from app.backtesting.indicators.indicators import TechnicalIndicators


class MACDStrategy(BaseStrategy):
    """MACD Strategy - Buy on bullish crossover, Sell on bearish crossover"""
    
    def __init__(self, parameters: Dict[str, Any]):
        """Initialize strategy with parameters"""
        default_params = {
            "fast_period": 12,
            "slow_period": 26,
            "signal_period": 9,
        }
        default_params.update(parameters)
        super().__init__("MACD Strategy", default_params)
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate signals based on MACD
        Buy when MACD > Signal line, Sell when MACD < Signal line
        """
        data = data.copy()
        
        fast = self.parameters.get("fast_period", 12)
        slow = self.parameters.get("slow_period", 26)
        signal = self.parameters.get("signal_period", 9)
        
        # Calculate MACD
        data["macd"], data["signal_line"], data["histogram"] = TechnicalIndicators.macd(
            data["close"], fast, slow, signal
        )
        
        # Generate signals
        data["signal"] = 0
        data.loc[data["macd"] > data["signal_line"], "signal"] = 1  # BUY
        data.loc[data["macd"] < data["signal_line"], "signal"] = -1  # SELL
        
        # Find signal changes
        data["position"] = data["signal"].diff()
        
        return data
