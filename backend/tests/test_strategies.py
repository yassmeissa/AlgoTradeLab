"""Tests for trading strategies"""

import pytest
import pandas as pd
import numpy as np
from app.backtesting.strategies import (
    MovingAverageCrossoverStrategy,
    RSIStrategy,
    MACDStrategy
)


@pytest.fixture
def sample_data():
    """Create sample OHLCV data"""
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    # Create trending data
    prices = np.linspace(100, 150, 100) + np.random.normal(0, 2, 100)
    data = pd.DataFrame({
        'open': prices,
        'high': prices + np.abs(np.random.normal(0, 1, 100)),
        'low': prices - np.abs(np.random.normal(0, 1, 100)),
        'close': prices,
        'volume': np.random.uniform(1000000, 2000000, 100)
    }, index=dates)
    return data


def test_moving_average_crossover_strategy(sample_data):
    """Test Moving Average Crossover strategy"""
    params = {"fast_period": 10, "slow_period": 20}
    strategy = MovingAverageCrossoverStrategy(params)
    signals = strategy.generate_signals(sample_data)
    
    assert 'signal' in signals.columns
    assert 'position' in signals.columns
    assert signals['signal'].isin([0, 1, -1]).all()


def test_rsi_strategy(sample_data):
    """Test RSI strategy"""
    params = {"rsi_period": 14, "oversold_threshold": 30, "overbought_threshold": 70}
    strategy = RSIStrategy(params)
    signals = strategy.generate_signals(sample_data)
    
    assert 'signal' in signals.columns
    assert 'rsi' in signals.columns
    assert signals['signal'].isin([0, 1, -1]).all()


def test_macd_strategy(sample_data):
    """Test MACD strategy"""
    params = {"fast_period": 12, "slow_period": 26, "signal_period": 9}
    strategy = MACDStrategy(params)
    signals = strategy.generate_signals(sample_data)
    
    assert 'signal' in signals.columns
    assert 'macd' in signals.columns
    assert 'signal_line' in signals.columns
    assert signals['signal'].isin([0, 1, -1]).all()
