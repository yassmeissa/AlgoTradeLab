"""Backtest service"""

from sqlalchemy.orm import Session
from typing import Dict, Any, Tuple
import json
import pandas as pd
from datetime import datetime
from app.models.backtest_result import BacktestResult
from app.models.strategy import Strategy
from app.backtesting.engine.backtest import BacktestEngine
from app.backtesting.strategies import (
    MovingAverageCrossoverStrategy,
    RSIStrategy,
    MACDStrategy,
)
from app.ml.ml_predictor import MLPredictor
from fastapi import HTTPException, status


class BacktestService:
    """Backtest business logic"""
    
    @staticmethod
    def get_strategy_class(strategy_type: str):
        """Get strategy class based on type"""
        strategies = {
            "moving_average_crossover": MovingAverageCrossoverStrategy,
            "rsi": RSIStrategy,
            "macd": MACDStrategy,
        }
        
        if strategy_type not in strategies:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown strategy type: {strategy_type}"
            )
        
        return strategies[strategy_type]
    
    @staticmethod
    def run_backtest(db: Session, strategy: Strategy, market_data: pd.DataFrame) -> BacktestResult:
        """Run a backtest"""
        
        # Parse strategy parameters
        parameters = json.loads(strategy.parameters)
        
        # Get strategy class and instantiate
        strategy_class = BacktestService.get_strategy_class(strategy.strategy_type)
        strategy_instance = strategy_class(parameters)
        
        # Create backtest engine
        engine = BacktestEngine(initial_capital=strategy.initial_capital)
        
        # Run backtest
        metrics, details = engine.run_backtest(market_data, strategy_instance)
        
        # Create result record
        result = BacktestResult(
            strategy_id=strategy.id,
            start_date=market_data.index[0],
            end_date=market_data.index[-1],
            total_return=metrics.total_return,
            roi=metrics.roi,
            sharpe_ratio=metrics.sharpe_ratio,
            max_drawdown=metrics.max_drawdown,
            win_rate=metrics.win_rate,
            profit_factor=metrics.profit_factor,
            total_trades=metrics.total_trades,
            winning_trades=metrics.winning_trades,
            losing_trades=metrics.losing_trades,
            average_trade=metrics.average_trade,
            best_trade=metrics.best_trade,
            worst_trade=metrics.worst_trade,
            trades=json.dumps(details["trades"]),
            equity_curve=json.dumps(details["equity_curve"]),
            status="completed"
        )
        
        db.add(result)
        db.commit()
        db.refresh(result)
        
        return result
    
    @staticmethod
    def run_ml_backtest(db: Session, strategy: Strategy, market_data: pd.DataFrame, model_type: str = "xgboost") -> BacktestResult:
        """Run backtest with ML predictions"""
        
        # Create ML predictor
        ml_predictor = MLPredictor(model_type=model_type)
        
        # Prepare and train model
        ml_predictor.train(market_data)
        
        # Get predictions
        signals_data = ml_predictor.predict(market_data)
        
        # Create backtest engine
        engine = BacktestEngine(initial_capital=strategy.initial_capital)
        
        # Run backtest with ML signals
        # For this, we need to adapt the engine to work with pre-computed signals
        metrics, details = engine.run_backtest(signals_data, type('obj', (object,), {'generate_signals': lambda self, data: data})())
        
        # Create result record
        result = BacktestResult(
            strategy_id=strategy.id,
            start_date=market_data.index[0],
            end_date=market_data.index[-1],
            total_return=metrics.total_return,
            roi=metrics.roi,
            sharpe_ratio=metrics.sharpe_ratio,
            max_drawdown=metrics.max_drawdown,
            win_rate=metrics.win_rate,
            profit_factor=metrics.profit_factor,
            total_trades=metrics.total_trades,
            winning_trades=metrics.winning_trades,
            losing_trades=metrics.losing_trades,
            average_trade=metrics.average_trade,
            best_trade=metrics.best_trade,
            worst_trade=metrics.worst_trade,
            trades=json.dumps(details["trades"]),
            equity_curve=json.dumps(details["equity_curve"]),
            status="completed"
        )
        
        db.add(result)
        db.commit()
        db.refresh(result)
        
        return result
    
    @staticmethod
    def get_backtest_result(db: Session, result_id: int, user_id: int) -> BacktestResult:
        """Get backtest result"""
        result = db.query(BacktestResult).join(Strategy).filter(
            BacktestResult.id == result_id,
            Strategy.user_id == user_id
        ).first()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Backtest result not found"
            )
        
        return result
    
    @staticmethod
    def list_backtest_results(db: Session, strategy_id: int, user_id: int):
        """List backtest results for a strategy"""
        results = db.query(BacktestResult).join(Strategy).filter(
            BacktestResult.strategy_id == strategy_id,
            Strategy.user_id == user_id
        ).all()
        
        return results
