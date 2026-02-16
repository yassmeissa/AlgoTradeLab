"""RSI Strategy"""

import pandas as pd
from typing import Dict, Any
from app.backtesting.strategies.base_strategy import BaseStrategy
from app.backtesting.indicators.indicators import TechnicalIndicators


class RSIStrategy(BaseStrategy):
    """RSI Strategy - Buy on oversold, Sell on overbought"""
    
    def __init__(self, parameters: Dict[str, Any]):
        """Initialize strategy with parameters"""
        default_params = {
            "rsi_period": 14,
            "oversold_threshold": 30,
            "overbought_threshold": 70,
        }
        default_params.update(parameters)
        super().__init__("RSI Strategy", default_params)
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate signals based on RSI
        Buy when RSI < oversold_threshold, Sell when RSI > overbought_threshold
        Hold between thresholds
        """
        data = data.copy()
        
        rsi_period = self.parameters.get("rsi_period", 14)
        oversold = self.parameters.get("oversold_threshold", 30)
        overbought = self.parameters.get("overbought_threshold", 70)
        
        # Validate parameters
        if not (0 < oversold < 50):
            raise ValueError("oversold_threshold should be between 0 and 50")
        if not (50 < overbought < 100):
            raise ValueError("overbought_threshold should be between 50 and 100")
        if oversold >= overbought:
            raise ValueError("oversold_threshold must be less than overbought_threshold")
        if rsi_period < 2:
            raise ValueError("rsi_period must be >= 2")
        
        # Calculate RSI
        data["rsi"] = TechnicalIndicators.rsi(data["close"], rsi_period)
        
        # Generate signals with hysteresis to avoid whipsaws
        data["signal"] = 0
        
        # Buy only on first touch of oversold
        data.loc[data["rsi"] < oversold, "signal"] = 1
        # Sell only on first touch of overbought
        data.loc[data["rsi"] > overbought, "signal"] = -1
        
        # Create crossover-only signals
        data["signal_change"] = data["signal"].diff()
        
        # Only trigger on state changes
        data.loc[data["signal_change"] == 0, "signal"] = 0
        
        # Fill NaN values
        data["signal"] = data["signal"].fillna(0).astype(int)
        
        return data
