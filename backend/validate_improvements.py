#!/usr/bin/env python3
"""
Validation Script for Backtesting Engine Improvements
This script validates all corrections and improvements
"""

import sys
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any


def create_sample_data(periods: int = 100) -> pd.DataFrame:
    """Create realistic sample OHLCV data"""
    dates = pd.date_range('2023-01-01', periods=periods, freq='D')
    prices = np.linspace(100, 150, periods)
    data = pd.DataFrame({
        'open': prices,
        'high': prices + 1,
        'low': prices - 1,
        'close': prices,
        'volume': np.ones(periods) * 1000000
    }, index=dates)
    return data


def validate_engine_initialization() -> bool:
    """Test 1: Engine initialization with different parameters"""
    print("\n✓ Test 1: Engine Initialization")
    try:
        from app.backtesting.engine.backtest import BacktestEngine
        
        # Test default
        engine1 = BacktestEngine()
        assert engine1.initial_capital == 10000.0
        assert engine1.commission == 0.001
        
        # Test custom
        engine2 = BacktestEngine(initial_capital=50000, commission=0.002, slippage=0.001)
        assert engine2.initial_capital == 50000
        assert engine2.commission == 0.002
        assert engine2.slippage == 0.001
        
        print("  ✅ Engine initialization working correctly")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False


def validate_signal_generation() -> bool:
    """Test 2: Strategy signal generation"""
    print("\n✓ Test 2: Signal Generation")
    try:
        from app.backtesting.strategies import MovingAverageCrossoverStrategy
        
        data = create_sample_data()
        strategy = MovingAverageCrossoverStrategy({"fast_period": 5, "slow_period": 10})
        signals = strategy.generate_signals(data.copy())
        
        # Check required columns
        assert "signal" in signals.columns, "Missing 'signal' column"
        assert "fast_ma" in signals.columns, "Missing 'fast_ma' column"
        assert "slow_ma" in signals.columns, "Missing 'slow_ma' column"
        
        # Check signal values
        assert signals["signal"].isin([-1, 0, 1]).all(), "Invalid signal values"
        
        # Check no NaN in signal (except first few)
        assert signals["signal"].iloc[10:].notna().sum() > 0
        
        print("  ✅ Signal generation working correctly")
        print(f"     - Generated {len(signals)} signals")
        print(f"     - Signal distribution: {signals['signal'].value_counts().to_dict()}")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_backtest_execution() -> bool:
    """Test 3: Backtest execution and metrics"""
    print("\n✓ Test 3: Backtest Execution")
    try:
        from app.backtesting.engine.backtest import BacktestEngine
        from app.backtesting.strategies import MovingAverageCrossoverStrategy
        
        data = create_sample_data()
        engine = BacktestEngine(initial_capital=10000, commission=0.001)
        strategy = MovingAverageCrossoverStrategy({"fast_period": 5, "slow_period": 10})
        
        metrics, details = engine.run_backtest(data, strategy)
        
        # Validate metrics
        assert metrics.total_return is not None
        assert metrics.roi is not None
        assert metrics.sharpe_ratio is not None
        assert metrics.max_drawdown is not None
        assert metrics.win_rate is not None
        
        # Validate details
        assert len(details['equity_curve']) == len(data)
        assert details['equity_curve'][0] == 10000  # Initial capital
        assert all(eq >= 0 for eq in details['equity_curve']), "Negative equity detected"
        
        print("  ✅ Backtest execution working correctly")
        print(f"     - ROI: {metrics.roi:.2f}%")
        print(f"     - Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
        print(f"     - Max Drawdown: {metrics.max_drawdown:.2f}%")
        print(f"     - Total Trades: {metrics.total_trades}")
        print(f"     - Win Rate: {metrics.win_rate:.2f}%")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_equity_curve_integrity() -> bool:
    """Test 4: Equity curve integrity"""
    print("\n✓ Test 4: Equity Curve Integrity")
    try:
        from app.backtesting.engine.backtest import BacktestEngine
        from app.backtesting.strategies import MovingAverageCrossoverStrategy
        
        data = create_sample_data()
        engine = BacktestEngine(initial_capital=10000)
        strategy = MovingAverageCrossoverStrategy({"fast_period": 5, "slow_period": 10})
        
        metrics, details = engine.run_backtest(data, strategy)
        equity = np.array(details['equity_curve'])
        
        # Check integrity
        assert equity[0] == 10000, "First equity should be initial capital"
        assert all(e >= 0 for e in equity), "Negative equity found"
        assert abs(metrics.total_return - (equity[-1] - 10000)) < 1, "ROI mismatch"
        
        print("  ✅ Equity curve integrity validated")
        print(f"     - Start: ${equity[0]:.2f}")
        print(f"     - End: ${equity[-1]:.2f}")
        print(f"     - Return: ${metrics.total_return:.2f}")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False


def validate_commission_impact() -> bool:
    """Test 5: Commission impact on returns"""
    print("\n✓ Test 5: Commission Impact")
    try:
        from app.backtesting.engine.backtest import BacktestEngine
        from app.backtesting.strategies import MovingAverageCrossoverStrategy
        
        data = create_sample_data()
        
        # Run without commission
        engine_no_comm = BacktestEngine(initial_capital=10000, commission=0.0)
        strategy = MovingAverageCrossoverStrategy({"fast_period": 5, "slow_period": 10})
        metrics_no_comm, _ = engine_no_comm.run_backtest(data, strategy)
        
        # Run with commission
        engine_with_comm = BacktestEngine(initial_capital=10000, commission=0.01)
        strategy2 = MovingAverageCrossoverStrategy({"fast_period": 5, "slow_period": 10})
        metrics_with_comm, _ = engine_with_comm.run_backtest(data, strategy2)
        
        # Commission should reduce returns
        assert metrics_no_comm.total_return >= metrics_with_comm.total_return, \
            "Commission should reduce returns"
        
        reduction = metrics_no_comm.total_return - metrics_with_comm.total_return
        print("  ✅ Commission impact validated")
        print(f"     - No commission ROI: {metrics_no_comm.roi:.2f}%")
        print(f"     - With commission ROI: {metrics_with_comm.roi:.2f}%")
        print(f"     - Reduction: ${reduction:.2f}")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_rsi_strategy() -> bool:
    """Test 6: RSI Strategy"""
    print("\n✓ Test 6: RSI Strategy")
    try:
        from app.backtesting.engine.backtest import BacktestEngine
        from app.backtesting.strategies import RSIStrategy
        
        data = create_sample_data()
        engine = BacktestEngine(initial_capital=10000)
        strategy = RSIStrategy({
            "rsi_period": 14,
            "oversold_threshold": 30,
            "overbought_threshold": 70
        })
        
        metrics, details = engine.run_backtest(data, strategy)
        
        assert metrics.total_trades >= 0
        assert 0 <= metrics.win_rate <= 100
        
        print("  ✅ RSI strategy working correctly")
        print(f"     - ROI: {metrics.roi:.2f}%")
        print(f"     - Total Trades: {metrics.total_trades}")
        print(f"     - Win Rate: {metrics.win_rate:.2f}%")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_slippage() -> bool:
    """Test 7: Slippage impact"""
    print("\n✓ Test 7: Slippage Impact")
    try:
        from app.backtesting.engine.backtest import BacktestEngine
        from app.backtesting.strategies import MovingAverageCrossoverStrategy
        
        data = create_sample_data()
        
        # Without slippage
        engine1 = BacktestEngine(initial_capital=10000, slippage=0.0)
        strategy1 = MovingAverageCrossoverStrategy({"fast_period": 5, "slow_period": 10})
        metrics1, _ = engine1.run_backtest(data, strategy1)
        
        # With slippage
        engine2 = BacktestEngine(initial_capital=10000, slippage=0.001)
        strategy2 = MovingAverageCrossoverStrategy({"fast_period": 5, "slow_period": 10})
        metrics2, _ = engine2.run_backtest(data, strategy2)
        
        # Slippage should reduce returns
        assert metrics1.total_return >= metrics2.total_return
        
        print("  ✅ Slippage impact validated")
        print(f"     - No slippage ROI: {metrics1.roi:.2f}%")
        print(f"     - With slippage ROI: {metrics2.roi:.2f}%")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("🧪 AlgoTrade Lab - Backtest Engine Validation")
    print("=" * 60)
    
    tests = [
        ("Engine Initialization", validate_engine_initialization),
        ("Signal Generation", validate_signal_generation),
        ("Backtest Execution", validate_backtest_execution),
        ("Equity Curve Integrity", validate_equity_curve_integrity),
        ("Commission Impact", validate_commission_impact),
        ("RSI Strategy", validate_rsi_strategy),
        ("Slippage Impact", validate_slippage),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} - Unexpected error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{'=' * 60}")
    print(f"Results: {passed}/{total} tests passed")
    print(f"{'=' * 60}\n")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
