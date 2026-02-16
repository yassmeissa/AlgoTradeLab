"""Data utilities for loading market data"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np


class DataProvider:
    """Market data provider"""
    
    @staticmethod
    def load_csv(filepath: str) -> pd.DataFrame:
        """Load market data from CSV file"""
        df = pd.read_csv(filepath, parse_dates=['timestamp'], index_col='timestamp')
        return df.sort_index()
    
    @staticmethod
    def generate_sample_data(start_date: datetime, end_date: datetime, symbol: str = "TEST") -> pd.DataFrame:
        """Generate sample OHLCV data for testing"""
        dates = pd.date_range(start_date, end_date, freq='D')
        
        # Generate realistic price movement with trend
        n = len(dates)
        trend = np.linspace(0, 10, n)
        noise = np.random.normal(0, 1, n)
        close_prices = 100 + trend + noise
        
        data = pd.DataFrame({
            'symbol': symbol,
            'open': close_prices + np.random.uniform(-0.5, 0.5, n),
            'high': close_prices + np.abs(np.random.normal(1, 0.5, n)),
            'low': close_prices - np.abs(np.random.normal(1, 0.5, n)),
            'close': close_prices,
            'volume': np.random.uniform(900000, 1100000, n)
        }, index=dates)
        
        data.index.name = 'timestamp'
        return data
    
    @staticmethod
    def resample_data(data: pd.DataFrame, frequency: str = 'H') -> pd.DataFrame:
        """Resample OHLCV data to different timeframe"""
        ohlc_dict = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }
        return data.resample(frequency).agg(ohlc_dict).dropna()
    
    @staticmethod
    def calculate_returns(data: pd.DataFrame) -> pd.Series:
        """Calculate daily returns"""
        return data['close'].pct_change()
