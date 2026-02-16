#!/usr/bin/env python3
"""
Complete Example: Using the Improved Backtesting Engine

This example demonstrates:
1. Creating sample data
2. Defining a strategy
3. Running a backtest
4. Analyzing results
5. Comparing different strategies
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def create_sample_market_data(days: int = 252, start_price: float = 100.0) -> pd.DataFrame:
    """
    Create realistic market data with trends and volatility
    
    Args:
        days: Number of trading days
        start_price: Initial price
    
    Returns:
        DataFrame with OHLCV data
    """
    dates = pd.date_range('2023-01-01', periods=days, freq='B')  # Business days
    
    # Create realistic price movements
    np.random.seed(42)
    returns = np.random.normal(0.0005, 0.015, days)  # Daily returns
    prices = start_price * np.exp(np.cumsum(returns))
    
    # Create OHLCV
    data = pd.DataFrame({
        'open': prices * (1 + np.random.uniform(-0.01, 0.01, days)),
        'high': prices * (1 + np.abs(np.random.uniform(0, 0.02, days))),
        'low': prices * (1 - np.abs(np.random.uniform(0, 0.02, days))),
        'close': prices,
        'volume': np.random.randint(1000000, 5000000, days)
    }, index=dates)
    
    # Ensure OHLC relationships
    data['high'] = data[['open', 'high', 'close']].max(axis=1)
    data['low'] = data[['open', 'low', 'close']].min(axis=1)
    
    return data


def example_1_basic_backtest():
    """Example 1: Basic backtest with Moving Average Crossover"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Moving Average Crossover Strategy")
    print("="*70)
    
    from app.backtesting.engine.backtest import BacktestEngine
    from app.backtesting.strategies import MovingAverageCrossoverStrategy
    
    # Create data
    data = create_sample_market_data(days=252)
    print(f"\n📊 Data: {len(data)} trading days ({data.index[0].date()} to {data.index[-1].date()})")
    print(f"   Price range: ${data['close'].min():.2f} - ${data['close'].max():.2f}")
    
    # Create strategy
    strategy = MovingAverageCrossoverStrategy({
        "fast_period": 10,
        "slow_period": 20
    })
    print(f"\n🎯 Strategy: Moving Average Crossover")
    print(f"   Fast MA: 10 days")
    print(f"   Slow MA: 20 days")
    
    # Run backtest
    engine = BacktestEngine(
        initial_capital=10000,
        commission=0.001,
        slippage=0.0005
    )
    
    metrics, details = engine.run_backtest(data, strategy)
    
    # Display results
    print(f"\n💰 Results:")
    print(f"   Initial Capital:    ${10000:.2f}")
    print(f"   Final Equity:       ${details['equity_curve'][-1]:.2f}")
    print(f"   Total Return:       ${metrics.total_return:.2f}")
    print(f"   ROI:                {metrics.roi:.2f}%")
    print(f"")
    print(f"📈 Performance Metrics:")
    print(f"   Sharpe Ratio:       {metrics.sharpe_ratio:.2f}")
    print(f"   Max Drawdown:       {metrics.max_drawdown:.2f}%")
    print(f"   Win Rate:           {metrics.win_rate:.2f}%")
    print(f"   Profit Factor:      {metrics.profit_factor:.2f}")
    print(f"")
    print(f"📊 Trade Statistics:")
    print(f"   Total Trades:       {metrics.total_trades}")
    print(f"   Winning Trades:     {metrics.winning_trades}")
    print(f"   Losing Trades:      {metrics.losing_trades}")
    print(f"   Average Trade:      ${metrics.average_trade:.2f}")
    print(f"   Best Trade:         ${metrics.best_trade:.2f}")
    print(f"   Worst Trade:        ${metrics.worst_trade:.2f}")
    
    if len(details['trades']) > 0:
        print(f"\n📋 First 5 Trades:")
        for i, trade in enumerate(details['trades'][:5]):
            print(f"\n   Trade {i+1}:")
            print(f"     Entry:  {trade['entry_date'].strftime('%Y-%m-%d')} @ ${trade['entry_price']:.2f}")
            print(f"     Exit:   {trade['exit_date'].strftime('%Y-%m-%d')} @ ${trade['exit_price']:.2f}")
            print(f"     PnL:    ${trade['pnl']:.2f} ({trade['pnl_percent']:.2f}%)")


def example_2_rsi_strategy():
    """Example 2: RSI Strategy"""
    print("\n" + "="*70)
    print("EXAMPLE 2: RSI Strategy (Mean Reversion)")
    print("="*70)
    
    from app.backtesting.engine.backtest import BacktestEngine
    from app.backtesting.strategies import RSIStrategy
    
    # Create data
    data = create_sample_market_data(days=252)
    
    # Create strategy
    strategy = RSIStrategy({
        "rsi_period": 14,
        "oversold_threshold": 30,
        "overbought_threshold": 70
    })
    print(f"\n🎯 Strategy: RSI (Mean Reversion)")
    print(f"   Period:             14")
    print(f"   Oversold (<):       30")
    print(f"   Overbought (>):     70")
    
    # Run backtest
    engine = BacktestEngine(initial_capital=10000, commission=0.001)
    metrics, details = engine.run_backtest(data, strategy)
    
    # Display results
    print(f"\n💰 Results:")
    print(f"   ROI:                {metrics.roi:.2f}%")
    print(f"   Sharpe Ratio:       {metrics.sharpe_ratio:.2f}")
    print(f"   Win Rate:           {metrics.win_rate:.2f}%")
    print(f"   Total Trades:       {metrics.total_trades}")


def example_3_parameter_optimization():
    """Example 3: Compare different parameters"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Parameter Optimization")
    print("="*70)
    
    from app.backtesting.engine.backtest import BacktestEngine
    from app.backtesting.strategies import MovingAverageCrossoverStrategy
    
    # Create data
    data = create_sample_market_data(days=252)
    
    # Test different parameters
    params_list = [
        {"fast_period": 5, "slow_period": 10},
        {"fast_period": 10, "slow_period": 20},
        {"fast_period": 15, "slow_period": 30},
        {"fast_period": 20, "slow_period": 50},
    ]
    
    print(f"\n🔍 Testing Different Parameters:")
    print(f"\n{'Fast':>8} {'Slow':>8} {'ROI':>10} {'Win Rate':>12} {'Trades':>10} {'Sharpe':>10}")
    print("-" * 60)
    
    results = []
    for params in params_list:
        strategy = MovingAverageCrossoverStrategy(params)
        engine = BacktestEngine(initial_capital=10000, commission=0.001)
        metrics, _ = engine.run_backtest(data, strategy)
        
        results.append({
            'params': params,
            'metrics': metrics
        })
        
        print(f"{params['fast_period']:>8} {params['slow_period']:>8} "
              f"{metrics.roi:>10.2f}% {metrics.win_rate:>12.2f}% "
              f"{metrics.total_trades:>10} {metrics.sharpe_ratio:>10.2f}")
    
    # Find best
    best = max(results, key=lambda x: x['metrics'].sharpe_ratio)
    print(f"\n✨ Best by Sharpe Ratio:")
    print(f"   Parameters: {best['params']}")
    print(f"   Sharpe Ratio: {best['metrics'].sharpe_ratio:.2f}")


def example_4_strategy_comparison():
    """Example 4: Compare strategies"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Strategy Comparison")
    print("="*70)
    
    from app.backtesting.engine.backtest import BacktestEngine
    from app.backtesting.strategies import MovingAverageCrossoverStrategy, RSIStrategy
    
    # Create data
    data = create_sample_market_data(days=252)
    
    strategies = {
        'Moving Average Crossover': MovingAverageCrossoverStrategy({
            "fast_period": 10,
            "slow_period": 20
        }),
        'RSI Mean Reversion': RSIStrategy({
            "rsi_period": 14,
            "oversold_threshold": 30,
            "overbought_threshold": 70
        })
    }
    
    print(f"\n📊 Comparing Strategies:")
    print(f"\n{'Strategy':30} {'ROI':>10} {'Sharpe':>10} {'Win Rate':>12} {'Trades':>10}")
    print("-" * 75)
    
    for name, strategy in strategies.items():
        engine = BacktestEngine(initial_capital=10000, commission=0.001)
        metrics, _ = engine.run_backtest(data, strategy)
        
        print(f"{name:30} {metrics.roi:>10.2f}% {metrics.sharpe_ratio:>10.2f} "
              f"{metrics.win_rate:>12.2f}% {metrics.total_trades:>10}")


def example_5_error_handling():
    """Example 5: Error handling and validation"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Error Handling and Validation")
    print("="*70)
    
    from app.backtesting.strategies import MovingAverageCrossoverStrategy
    
    print(f"\n🔍 Testing Parameter Validation:")
    
    # Test 1: Invalid parameters
    print(f"\n1️⃣ Invalid Parameters (fast >= slow):")
    try:
        strategy = MovingAverageCrossoverStrategy({
            "fast_period": 20,
            "slow_period": 10
        })
        print("   ❌ Should have raised error!")
    except ValueError as e:
        print(f"   ✅ Caught error: {e}")
    
    # Test 2: Valid parameters
    print(f"\n2️⃣ Valid Parameters (fast < slow):")
    try:
        strategy = MovingAverageCrossoverStrategy({
            "fast_period": 10,
            "slow_period": 20
        })
        print(f"   ✅ Strategy created successfully")
    except ValueError as e:
        print(f"   ❌ Unexpected error: {e}")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("🚀 AlgoTrade Lab - Backtesting Engine Examples")
    print("="*70)
    
    try:
        # Run examples
        example_1_basic_backtest()
        example_2_rsi_strategy()
        example_3_parameter_optimization()
        example_4_strategy_comparison()
        example_5_error_handling()
        
        print("\n" + "="*70)
        print("✅ All examples completed successfully!")
        print("="*70 + "\n")
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
