"""Tests for technical indicators"""

import pytest
import pandas as pd
import numpy as np
from app.backtesting.indicators.indicators import TechnicalIndicators


@pytest.fixture
def sample_data():
    """Create sample OHLCV data"""
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    data = pd.DataFrame({
        'open': np.random.uniform(100, 110, 100),
        'high': np.random.uniform(110, 120, 100),
        'low': np.random.uniform(90, 100, 100),
        'close': np.random.uniform(100, 110, 100),
        'volume': np.random.uniform(1000000, 2000000, 100)
    }, index=dates)
    return data


def test_moving_average(sample_data):
    """Test simple moving average"""
    ma = TechnicalIndicators.moving_average(sample_data['close'], 10)
    assert len(ma) == len(sample_data)
    assert ma.isna().sum() == 9  # First 9 values should be NaN


def test_exponential_moving_average(sample_data):
    """Test exponential moving average"""
    ema = TechnicalIndicators.exponential_moving_average(sample_data['close'], 10)
    assert len(ema) == len(sample_data)


def test_rsi(sample_data):
    """Test RSI indicator"""
    rsi = TechnicalIndicators.rsi(sample_data['close'], 14)
    assert len(rsi) == len(sample_data)
    # RSI should be between 0 and 100
    assert (rsi[~rsi.isna()] >= 0).all()
    assert (rsi[~rsi.isna()] <= 100).all()


def test_macd(sample_data):
    """Test MACD indicator"""
    macd, signal, histogram = TechnicalIndicators.macd(sample_data['close'])
    assert len(macd) == len(sample_data)
    assert len(signal) == len(sample_data)
    assert len(histogram) == len(sample_data)


def test_bollinger_bands(sample_data):
    """Test Bollinger Bands"""
    upper, middle, lower = TechnicalIndicators.bollinger_bands(sample_data['close'])
    assert len(upper) == len(sample_data)
    assert len(middle) == len(sample_data)
    assert len(lower) == len(sample_data)
    # Upper band should always be >= middle band >= lower band
    assert (upper[~upper.isna()] >= middle[~middle.isna()]).all()
    assert (middle[~middle.isna()] >= lower[~lower.isna()]).all()
