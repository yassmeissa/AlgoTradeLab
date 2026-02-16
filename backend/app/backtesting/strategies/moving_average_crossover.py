"""Moving Average Crossover Strategy"""

import pandas as pd
from typing import Dict, Any
from app.backtesting.strategies.base_strategy import BaseStrategy
from app.backtesting.indicators.indicators import TechnicalIndicators


class MovingAverageCrossoverStrategy(BaseStrategy):
    """Moving Average Crossover Strategy"""
    
    def __init__(self, parameters: Dict[str, Any]):
        """Initialize strategy with parameters"""
        default_params = {
            "fast_period": 10,
            "slow_period": 20,
        }
        default_params.update(parameters)
        super().__init__("Moving Average Crossover", default_params)
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate signals based on moving average crossover
        Buy when fast MA > slow MA, Sell when fast MA < slow MA
        """
        data = data.copy()
        
        fast_period = self.parameters.get("fast_period", 10)
        slow_period = self.parameters.get("slow_period", 20)
        
        # Validate periods
        if fast_period >= slow_period:
            raise ValueError("fast_period must be less than slow_period")
        if fast_period < 1 or slow_period < 2:
            raise ValueError("periods must be >= 1")
        
        # Calculate moving averages
        data["fast_ma"] = TechnicalIndicators.moving_average(data["close"], fast_period)
        data["slow_ma"] = TechnicalIndicators.moving_average(data["close"], slow_period)
        
        # Generate initial signals based on MA relationship
        data["signal"] = 0
        data.loc[data["fast_ma"] > data["slow_ma"], "signal"] = 1  # BUY
        data.loc[data["fast_ma"] < data["slow_ma"], "signal"] = -1  # SELL
        
        # Only trigger on crossovers (signal changes), not continuous holding
        data["signal_change"] = data["signal"].diff()
        
        # Reset signal to 0 except on crossover points
        data.loc[data["signal_change"] == 0, "signal"] = 0
        data.loc[data["signal_change"].notna() & (data["signal_change"] != 0), "signal"] = data.loc[data["signal_change"].notna() & (data["signal_change"] != 0), "signal"]
        
        # Fill NaN at the beginning with 0
        data["signal"] = data["signal"].fillna(0).astype(int)
        
        return data
