"""Performance calculations and analytics"""

import numpy as np
import pandas as pd
from typing import Tuple


class PerformanceCalculator:
    """Calculate performance metrics"""
    
    @staticmethod
    def calculate_returns(equity_curve: np.ndarray) -> np.ndarray:
        """Calculate daily returns"""
        return np.diff(equity_curve) / equity_curve[:-1]
    
    @staticmethod
    def calculate_cumulative_returns(equity_curve: np.ndarray, initial_capital: float) -> np.ndarray:
        """Calculate cumulative returns"""
        return (equity_curve - initial_capital) / initial_capital
    
    @staticmethod
    def calculate_drawdown(equity_curve: np.ndarray) -> Tuple[np.ndarray, float]:
        """Calculate drawdown series and max drawdown"""
        running_max = np.maximum.accumulate(equity_curve)
        drawdown = (equity_curve - running_max) / running_max
        max_drawdown = np.min(drawdown)
        return drawdown, max_drawdown
    
    @staticmethod
    def calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe Ratio"""
        if len(returns) == 0 or np.std(returns) == 0:
            return 0
        
        excess_returns = returns - (risk_free_rate / 252)
        sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
        return float(sharpe)
    
    @staticmethod
    def calculate_sortino_ratio(returns: np.ndarray, risk_free_rate: float = 0.02, target_return: float = 0) -> float:
        """Calculate Sortino Ratio (only penalizes downside volatility)"""
        if len(returns) == 0:
            return 0
        
        excess_returns = returns - (risk_free_rate / 252)
        downside_returns = np.minimum(excess_returns - target_return, 0)
        downside_std = np.std(downside_returns)
        
        if downside_std == 0:
            return 0
        
        sortino = np.mean(excess_returns) / downside_std * np.sqrt(252)
        return float(sortino)
    
    @staticmethod
    def calculate_calmar_ratio(returns: np.ndarray, equity_curve: np.ndarray) -> float:
        """Calculate Calmar Ratio"""
        annual_return = np.mean(returns) * 252
        
        _, max_dd = PerformanceCalculator.calculate_drawdown(equity_curve)
        
        if abs(max_dd) < 1e-6:
            return 0
        
        calmar = annual_return / abs(max_dd)
        return float(calmar)
    
    @staticmethod
    def calculate_win_rate(trades: list) -> float:
        """Calculate win rate percentage"""
        if len(trades) == 0:
            return 0
        
        winning_trades = sum(1 for t in trades if t['pnl'] > 0)
        return (winning_trades / len(trades)) * 100
    
    @staticmethod
    def calculate_profit_factor(trades: list) -> float:
        """Calculate profit factor"""
        if len(trades) == 0:
            return 0
        
        total_profit = sum(t['pnl'] for t in trades if t['pnl'] > 0)
        total_loss = abs(sum(t['pnl'] for t in trades if t['pnl'] < 0))
        
        if total_loss < 1e-6:
            return 0 if total_profit < 1e-6 else float('inf')
        
        return total_profit / total_loss


class RiskMetrics:
    """Calculate risk metrics"""
    
    @staticmethod
    def value_at_risk(returns: np.ndarray, confidence_level: float = 0.95) -> float:
        """Calculate Value at Risk"""
        return np.percentile(returns, (1 - confidence_level) * 100)
    
    @staticmethod
    def conditional_value_at_risk(returns: np.ndarray, confidence_level: float = 0.95) -> float:
        """Calculate Conditional Value at Risk (expected shortfall)"""
        var = RiskMetrics.value_at_risk(returns, confidence_level)
        return returns[returns <= var].mean()
    
    @staticmethod
    def max_consecutive_losses(trades: list) -> int:
        """Calculate maximum consecutive losing trades"""
        if len(trades) == 0:
            return 0
        
        max_consec = 0
        current_consec = 0
        
        for trade in trades:
            if trade['pnl'] < 0:
                current_consec += 1
                max_consec = max(max_consec, current_consec)
            else:
                current_consec = 0
        
        return max_consec
    
    @staticmethod
    def recovery_factor(total_return: float, max_drawdown: float) -> float:
        """Calculate recovery factor"""
        if abs(max_drawdown) < 1e-6:
            return 0
        
        return total_return / abs(max_drawdown)


class TradeAnalytics:
    """Analyze trade statistics"""
    
    @staticmethod
    def calculate_average_win(trades: list) -> float:
        """Calculate average winning trade"""
        winning_trades = [t['pnl'] for t in trades if t['pnl'] > 0]
        return np.mean(winning_trades) if winning_trades else 0
    
    @staticmethod
    def calculate_average_loss(trades: list) -> float:
        """Calculate average losing trade"""
        losing_trades = [t['pnl'] for t in trades if t['pnl'] < 0]
        return np.mean(losing_trades) if losing_trades else 0
    
    @staticmethod
    def calculate_expectancy(trades: list, win_rate: float) -> float:
        """Calculate expectancy (average trade value)"""
        if len(trades) == 0:
            return 0
        
        avg_win = TradeAnalytics.calculate_average_win(trades)
        avg_loss = TradeAnalytics.calculate_average_loss(trades)
        
        win_prob = win_rate / 100
        loss_prob = 1 - win_prob
        
        return (win_prob * avg_win) + (loss_prob * avg_loss)
    
    @staticmethod
    def calculate_payoff_ratio(trades: list) -> float:
        """Calculate payoff ratio (average win / average loss)"""
        avg_win = TradeAnalytics.calculate_average_win(trades)
        avg_loss = abs(TradeAnalytics.calculate_average_loss(trades))
        
        if avg_loss < 1e-6:
            return 0
        
        return avg_win / avg_loss
