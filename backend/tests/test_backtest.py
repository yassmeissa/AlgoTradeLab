"""Tests for backtesting engine"""

import pytest
import pandas as pd
import numpy as np
from app.backtesting.engine.backtest import BacktestEngine, BacktestMetrics
from app.backtesting.strategies import MovingAverageCrossoverStrategy, RSIStrategy


@pytest.fixture
def sample_data():
    """Create sample OHLCV data with clear trends"""
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    # Create trending data with clear patterns
    prices = np.linspace(100, 150, 100)
    data = pd.DataFrame({
        'open': prices,
        'high': prices + 1,
        'low': prices - 1,
        'close': prices,
        'volume': np.ones(100) * 1000000
    }, index=dates)
    return data


@pytest.fixture
def volatile_data():
    """Create volatile data for testing"""
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    # Create volatile data
    np.random.seed(42)
    prices = 100 + np.cumsum(np.random.randn(100) * 2)
    data = pd.DataFrame({
        'open': prices,
        'high': prices + np.abs(np.random.randn(100)),
        'low': prices - np.abs(np.random.randn(100)),
        'close': prices,
        'volume': np.random.randint(500000, 1500000, 100)
    }, index=dates)
    return data


def test_backtest_engine_initialization():
    """Test BacktestEngine initialization"""
    engine = BacktestEngine(initial_capital=10000, commission=0.001)
    assert engine.initial_capital == 10000
    assert engine.commission == 0.001
    assert engine.slippage == 0.0


def test_backtest_engine_with_slippage():
    """Test BacktestEngine with slippage"""
    engine = BacktestEngine(initial_capital=10000, slippage=0.001)
    assert engine.slippage == 0.001


def test_run_backtest_with_mac(sample_data):
    """Test running a backtest with Moving Average Crossover"""
    engine = BacktestEngine(initial_capital=10000, commission=0.001)
    strategy = MovingAverageCrossoverStrategy({"fast_period": 10, "slow_period": 20})
    
    metrics, details = engine.run_backtest(sample_data, strategy)
    
    assert isinstance(metrics, BacktestMetrics)
    assert metrics.roi is not None
    assert metrics.sharpe_ratio is not None
    assert metrics.max_drawdown is not None
    assert metrics.win_rate is not None
    assert details['equity_curve'] is not None
    assert len(details['trades']) >= 0
    assert len(details['equity_curve']) == len(sample_data)


def test_run_backtest_with_rsi(sample_data):
    """Test running a backtest with RSI Strategy"""
    engine = BacktestEngine(initial_capital=10000, commission=0.001)
    strategy = RSIStrategy({"rsi_period": 14, "oversold_threshold": 30, "overbought_threshold": 70})
    
    metrics, details = engine.run_backtest(sample_data, strategy)
    
    assert isinstance(metrics, BacktestMetrics)
    assert metrics.total_trades >= 0
    assert metrics.winning_trades <= metrics.total_trades
    assert metrics.losing_trades <= metrics.total_trades


def test_equity_curve_integrity(sample_data):
    """Test that equity curve is properly calculated"""
    engine = BacktestEngine(initial_capital=10000)
    strategy = MovingAverageCrossoverStrategy({"fast_period": 5, "slow_period": 10})
    
    metrics, details = engine.run_backtest(sample_data, strategy)
    
    equity = np.array(details['equity_curve'])
    
    # First value should be initial capital
    assert equity[0] == 10000
    # Equity should not be negative
    assert np.all(equity >= 0)
    # Final equity should be close to calculated ROI
    assert metrics.total_return == equity[-1] - 10000


def test_calculate_sharpe_ratio():
    """Test Sharpe Ratio calculation"""
    returns = np.random.normal(0.001, 0.02, 252)
    sharpe = BacktestEngine._calculate_sharpe_ratio(returns)
    assert isinstance(sharpe, float)
    assert not np.isnan(sharpe)


def test_calculate_sharpe_ratio_zero_returns():
    """Test Sharpe Ratio with zero returns"""
    returns = np.zeros(252)
    sharpe = BacktestEngine._calculate_sharpe_ratio(returns)
    assert sharpe == 0


def test_calculate_max_drawdown():
    """Test Maximum Drawdown calculation"""
    equity = np.array([10000, 11000, 10500, 12000, 11000, 13000])
    max_dd = BacktestEngine._calculate_max_drawdown(equity)
    assert isinstance(max_dd, float)
    assert max_dd < 0  # Drawdown should be negative


def test_calculate_max_drawdown_no_drawdown():
    """Test Maximum Drawdown with only gains"""
    equity = np.array([10000, 11000, 12000, 13000, 14000])
    max_dd = BacktestEngine._calculate_max_drawdown(equity)
    assert max_dd == 0  # No drawdown


def test_trades_recorded_correctly(sample_data):
    """Test that trades are recorded correctly"""
    engine = BacktestEngine(initial_capital=10000, commission=0.001)
    strategy = MovingAverageCrossoverStrategy({"fast_period": 5, "slow_period": 15})
    
    metrics, details = engine.run_backtest(sample_data, strategy)
    
    # Check trades structure
    for trade in details['trades']:
        assert 'entry_date' in trade
        assert 'entry_price' in trade
        assert 'exit_date' in trade
        assert 'exit_price' in trade
        assert 'quantity' in trade
        assert 'pnl' in trade
        assert 'pnl_percent' in trade
        assert trade['quantity'] > 0


def test_commission_impact(sample_data):
    """Test that commission reduces returns"""
    engine_no_comm = BacktestEngine(initial_capital=10000, commission=0.0)
    engine_with_comm = BacktestEngine(initial_capital=10000, commission=0.01)
    
    strategy = MovingAverageCrossoverStrategy({"fast_period": 5, "slow_period": 15})
    
    metrics_no_comm, _ = engine_no_comm.run_backtest(sample_data, strategy)
    metrics_with_comm, _ = engine_with_comm.run_backtest(sample_data, strategy)
    
    # Commission should reduce returns
    assert metrics_no_comm.total_return >= metrics_with_comm.total_return


def test_mac_strategy_parameter_validation():
    """Test MAC strategy parameter validation"""
    with pytest.raises(ValueError):
        strategy = MovingAverageCrossoverStrategy({"fast_period": 20, "slow_period": 10})
        # Fast period >= slow period should fail


def test_rsi_strategy_parameter_validation():
    """Test RSI strategy parameter validation"""
    with pytest.raises(ValueError):
        strategy = RSIStrategy({"oversold_threshold": 70, "overbought_threshold": 30})
        # Oversold >= overbought should fail
