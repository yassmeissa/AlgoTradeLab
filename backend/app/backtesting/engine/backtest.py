"""Main backtesting engine"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class BacktestMetrics:
    """Backtest performance metrics"""
    total_return: float
    roi: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    average_trade: float
    best_trade: float
    worst_trade: float


class BacktestEngine:
    """Core backtesting engine"""
    
    def __init__(self, initial_capital: float = 10000.0, commission: float = 0.001, slippage: float = 0.0):
        """
        Initialize backtesting engine
        
        Args:
            initial_capital: Starting capital
            commission: Commission per trade (0.001 = 0.1%)
            slippage: Price slippage percentage
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.trades = []
        self.equity_curve = []
    
    def run_backtest(self, data: pd.DataFrame, strategy) -> Tuple[BacktestMetrics, Dict[str, Any]]:
        """
        Run backtest on data with given strategy
        
        Args:
            data: DataFrame with OHLCV data
            strategy: Strategy object with generate_signals method
        
        Returns:
            Tuple of (metrics, details)
        """
        # Generate signals
        signals_data = strategy.generate_signals(data.copy())
        
        # Execute trades and calculate equity
        equity = self._execute_trades(signals_data)
        
        # Calculate metrics
        metrics = self._calculate_metrics(equity, signals_data)
        
        # Prepare details
        details = {
            "trades": [asdict(t) for t in self.trades],
            "equity_curve": equity.tolist(),
            "timestamps": data.index.tolist(),
        }
        
        return metrics, details
    
    def _execute_trades(self, signals_data: pd.DataFrame) -> np.ndarray:
        """Execute trades based on signals and calculate equity curve"""
        equity = np.zeros(len(signals_data))
        equity[0] = self.initial_capital
        
        position = 0
        position_value = 0  # Value of open position
        entry_price = 0
        entry_date = None
        cash = self.initial_capital
        
        for i in range(len(signals_data)):
            current_price = signals_data["close"].iloc[i]
            
            # Check for entry signal (BUY)
            if signals_data["signal"].iloc[i] == 1 and position == 0:
                # Enter long position
                entry_price = current_price * (1 + self.slippage)
                entry_date = signals_data.index[i]
                quantity = int(cash / entry_price)
                
                if quantity > 0:
                    position = quantity
                    position_value = quantity * entry_price
                    cash -= position_value
            
            # Check for exit signal (SELL)
            elif signals_data["signal"].iloc[i] == -1 and position > 0:
                # Exit long position
                exit_price = current_price * (1 - self.slippage)
                exit_date = signals_data.index[i]
                
                # Calculate PnL
                gross_pnl = (exit_price - entry_price) * position
                commission_cost = (position_value + position * exit_price) * self.commission
                net_pnl = gross_pnl - commission_cost
                
                # Update cash
                cash += position * exit_price + net_pnl
                
                # Record trade
                trade = {
                    "entry_date": entry_date,
                    "entry_price": entry_price,
                    "exit_date": exit_date,
                    "exit_price": exit_price,
                    "quantity": position,
                    "side": "BUY",
                    "pnl": net_pnl,
                    "pnl_percent": (net_pnl / position_value) * 100 if position_value > 0 else 0
                }
                self.trades.append(trade)
                
                position = 0
                position_value = 0
            
            # Calculate equity (Mark-to-Market)
            if position > 0:
                mtm_value = position * current_price
                equity[i] = cash + mtm_value
            else:
                equity[i] = cash
        
        # Close any open positions at the end
        if position > 0:
            exit_price = signals_data["close"].iloc[-1] * (1 - self.slippage)
            pnl = (exit_price - entry_price) * position
            commission_cost = (position_value + position * exit_price) * self.commission
            net_pnl = pnl - commission_cost
            
            trade = {
                "entry_date": entry_date,
                "entry_price": entry_price,
                "exit_date": signals_data.index[-1],
                "exit_price": exit_price,
                "quantity": position,
                "side": "BUY",
                "pnl": net_pnl,
                "pnl_percent": (net_pnl / position_value) * 100 if position_value > 0 else 0
            }
            self.trades.append(trade)
            
            # Final equity with closed position
            equity[-1] = cash + position * exit_price
        
        self.equity_curve = equity
        return equity
    
    def _calculate_metrics(self, equity: np.ndarray, signals_data: pd.DataFrame) -> BacktestMetrics:
        """Calculate performance metrics"""
        
        # Returns
        total_return = equity[-1] - self.initial_capital
        roi = (total_return / self.initial_capital) * 100
        
        # Sharpe Ratio
        returns = np.diff(equity) / equity[:-1]
        sharpe_ratio = self._calculate_sharpe_ratio(returns)
        
        # Maximum Drawdown
        max_drawdown = self._calculate_max_drawdown(equity)
        
        # Trade statistics
        if len(self.trades) > 0:
            pnls = [t["pnl"] for t in self.trades]
            winning_trades = len([t for t in self.trades if t["pnl"] > 0])
            losing_trades = len([t for t in self.trades if t["pnl"] < 0])
            win_rate = (winning_trades / len(self.trades)) * 100 if len(self.trades) > 0 else 0
            
            total_profit = sum([t["pnl"] for t in self.trades if t["pnl"] > 0])
            total_loss = abs(sum([t["pnl"] for t in self.trades if t["pnl"] < 0]))
            profit_factor = total_profit / total_loss if total_loss > 0 else 0
            
            average_trade = np.mean(pnls)
            best_trade = max(pnls)
            worst_trade = min(pnls)
        else:
            winning_trades = losing_trades = 0
            win_rate = profit_factor = average_trade = 0
            best_trade = worst_trade = 0
        
        metrics = BacktestMetrics(
            total_return=total_return,
            roi=roi,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            profit_factor=profit_factor,
            total_trades=len(self.trades),
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            average_trade=average_trade,
            best_trade=best_trade,
            worst_trade=worst_trade,
        )
        
        return metrics
    
    @staticmethod
    def _calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe Ratio"""
        if len(returns) == 0 or np.std(returns) == 0:
            return 0
        
        excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
        sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
        
        return float(sharpe_ratio)
    
    @staticmethod
    def _calculate_max_drawdown(equity: np.ndarray) -> float:
        """Calculate maximum drawdown"""
        running_max = np.maximum.accumulate(equity)
        drawdown = (equity - running_max) / running_max
        max_drawdown = np.min(drawdown) * 100
        
        return float(max_drawdown)
