"""
Enhanced backtest routes with detailed Swagger documentation
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from datetime import datetime
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/backtests", tags=["📊 Backtests"])


# ============================================================================
# Request Models with Swagger documentation
# ============================================================================

class BacktestRequestModel(BaseModel):
    """
    Backtest Request Model
    
    Parameters for running a backtest on a strategy with market data.
    """
    strategy_id: int = Field(
        ...,
        description="ID of the strategy to backtest",
        example=1,
        gt=0
    )
    symbol: str = Field(
        ...,
        description="Stock ticker symbol",
        example="AAPL",
        min_length=1,
        max_length=10
    )
    start_date: str = Field(
        ...,
        description="Start date in YYYY-MM-DD format",
        example="2023-01-01",
        regex="^\d{4}-\d{2}-\d{2}$"
    )
    end_date: str = Field(
        ...,
        description="End date in YYYY-MM-DD format",
        example="2023-12-31",
        regex="^\d{4}-\d{2}-\d{2}$"
    )
    initial_capital: float = Field(
        default=10000.0,
        description="Starting capital for the backtest",
        example=10000.0,
        gt=0
    )
    commission: float = Field(
        default=0.001,
        description="Commission per trade (0.001 = 0.1%)",
        example=0.001,
        ge=0,
        le=1
    )
    slippage: float = Field(
        default=0.0005,
        description="Price slippage as decimal percentage",
        example=0.0005,
        ge=0,
        le=1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "strategy_id": 1,
                "symbol": "AAPL",
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "initial_capital": 10000,
                "commission": 0.001,
                "slippage": 0.0005
            }
        }


class TradeModel(BaseModel):
    """Individual trade details"""
    entry_date: str = Field(..., description="Trade entry date")
    entry_price: float = Field(..., description="Entry price per unit")
    exit_date: str = Field(..., description="Trade exit date")
    exit_price: float = Field(..., description="Exit price per unit")
    quantity: int = Field(..., description="Number of units traded")
    side: str = Field(..., description="Trade side (BUY/SELL)")
    pnl: float = Field(..., description="Profit/Loss in currency")
    pnl_percent: float = Field(..., description="Profit/Loss percentage")


class BacktestResultModel(BaseModel):
    """
    Backtest Result Model
    
    Complete backtest results including metrics and trade history.
    """
    id: int = Field(..., description="Backtest result ID")
    strategy_id: int = Field(..., description="Associated strategy ID")
    user_id: int = Field(..., description="User who ran the backtest")
    
    # Performance Metrics
    total_return: float = Field(
        ...,
        description="Absolute return amount in currency"
    )
    roi: float = Field(
        ...,
        description="Return on Investment as percentage (0-100)"
    )
    sharpe_ratio: float = Field(
        ...,
        description="Risk-adjusted return (Sharpe ratio). Higher is better"
    )
    max_drawdown: float = Field(
        ...,
        description="Maximum peak-to-trough decline as percentage"
    )
    win_rate: float = Field(
        ...,
        description="Percentage of winning trades (0-100)"
    )
    profit_factor: float = Field(
        ...,
        description="Total profit / Total loss ratio"
    )
    
    # Trade Statistics
    total_trades: int = Field(..., description="Total number of trades")
    winning_trades: int = Field(..., description="Number of profitable trades")
    losing_trades: int = Field(..., description="Number of losing trades")
    average_trade: float = Field(..., description="Average profit/loss per trade")
    best_trade: float = Field(..., description="Best single trade profit")
    worst_trade: float = Field(..., description="Worst single trade loss")
    
    # Trade and Equity Data
    trades: List[TradeModel] = Field(
        default=[],
        description="Detailed history of all trades"
    )
    equity_curve: List[float] = Field(
        default=[],
        description="Portfolio equity value at each time step"
    )
    
    # Metadata
    created_at: str = Field(..., description="Result creation timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "strategy_id": 1,
                "user_id": 1,
                "total_return": 875.50,
                "roi": 8.75,
                "sharpe_ratio": 1.23,
                "max_drawdown": -7.5,
                "win_rate": 62.5,
                "profit_factor": 3.5,
                "total_trades": 8,
                "winning_trades": 5,
                "losing_trades": 3,
                "average_trade": 109.44,
                "best_trade": 250.00,
                "worst_trade": -75.00,
                "trades": [],
                "equity_curve": [10000, 10100, 10200],
                "created_at": "2024-02-16T10:30:00Z"
            }
        }


# ============================================================================
# Route Handlers with Swagger documentation
# ============================================================================

@router.post(
    "/run",
    response_model=BacktestResultModel,
    summary="Run Backtest",
    description="""
    Execute a backtest for a given strategy on historical market data.
    
    **Process:**
    1. Fetches historical OHLCV data for the specified date range
    2. Generates trading signals using the strategy
    3. Simulates trade execution with commission and slippage
    4. Calculates performance metrics (ROI, Sharpe, Drawdown, etc)
    5. Returns detailed results and trade history
    
    **Requirements:**
    - Valid JWT token in Authorization header
    - Strategy must exist and belong to authenticated user
    - Date range must be valid (start < end)
    - Initial capital must be positive
    
    **Performance Metrics Explained:**
    - **ROI**: Total return as percentage
    - **Sharpe Ratio**: Risk-adjusted returns (higher is better)
    - **Max Drawdown**: Largest peak-to-trough decline
    - **Win Rate**: % of trades that were profitable
    - **Profit Factor**: Total profit / Total loss ratio
    """,
    responses={
        200: {
            "description": "Backtest completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "strategy_id": 1,
                        "user_id": 1,
                        "total_return": 875.50,
                        "roi": 8.75,
                        "sharpe_ratio": 1.23,
                        "max_drawdown": -7.5,
                        "win_rate": 62.5,
                        "profit_factor": 3.5,
                        "total_trades": 8,
                        "winning_trades": 5,
                        "losing_trades": 3,
                        "average_trade": 109.44,
                        "best_trade": 250.00,
                        "worst_trade": -75.00,
                        "created_at": "2024-02-16T10:30:00Z"
                    }
                }
            }
        },
        401: {"description": "Unauthorized - Invalid or missing token"},
        404: {"description": "Strategy not found"},
        422: {"description": "Validation error - Check request parameters"}
    }
)
def run_backtest(
    request: BacktestRequestModel,
    authorization: str = Header(..., description="JWT Bearer token")
):
    """
    Run a backtest
    
    **Required Header:**
    - Authorization: Bearer <jwt_token>
    """
    pass


@router.get(
    "/{result_id}",
    response_model=BacktestResultModel,
    summary="Get Backtest Result",
    description="""
    Retrieve a previously executed backtest result by ID.
    
    **Returns:**
    - Complete backtest metrics
    - Detailed trade history
    - Equity curve over time
    """,
    responses={
        200: {"description": "Backtest result retrieved successfully"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        404: {"description": "Backtest result not found"}
    }
)
def get_backtest_result(
    result_id: int = Field(..., description="Backtest result ID", gt=0),
    authorization: str = Header(..., description="JWT Bearer token")
):
    """Get backtest result by ID"""
    pass


@router.get(
    "",
    response_model=List[BacktestResultModel],
    summary="List Backtest Results",
    description="""
    List all backtest results for the authenticated user.
    
    **Returns:**
    - Array of backtest results
    - Sorted by creation date (newest first)
    - Limited to user's own results
    """,
    responses={
        200: {"description": "List of backtest results"},
        401: {"description": "Unauthorized - Invalid or missing token"}
    }
)
def list_backtest_results(
    skip: int = Field(0, ge=0, description="Number of results to skip"),
    limit: int = Field(10, ge=1, le=100, description="Max results to return"),
    authorization: str = Header(..., description="JWT Bearer token")
):
    """List backtest results for current user"""
    pass


@router.delete(
    "/{result_id}",
    summary="Delete Backtest Result",
    description="Delete a backtest result by ID",
    responses={
        204: {"description": "Backtest result deleted successfully"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        404: {"description": "Backtest result not found"}
    }
)
def delete_backtest_result(
    result_id: int = Field(..., description="Backtest result ID", gt=0),
    authorization: str = Header(..., description="JWT Bearer token")
):
    """Delete backtest result"""
    pass
