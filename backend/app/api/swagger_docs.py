"""
Swagger/OpenAPI Documentation for AlgoTrade Lab API

This file provides detailed OpenAPI schema information for Swagger documentation.
FastAPI automatically generates Swagger UI at /docs and ReDoc at /redoc
"""

# Tags metadata for better organization in Swagger
TAGS_METADATA = [
    {
        "name": "🔐 Authentication",
        "description": """
        Authentication endpoints for user management and JWT token handling.
        
        **Features:**
        - User registration and login
        - JWT token generation and validation
        - Token refresh functionality
        - Secure password management
        """,
    },
    {
        "name": "🎯 Strategies",
        "description": """
        Strategy management endpoints for creating, reading, and updating trading strategies.
        
        **Supported Strategies:**
        - Moving Average Crossover (MAC)
        - RSI (Relative Strength Index)
        - MACD (Moving Average Convergence Divergence)
        - Custom strategies (extensible)
        
        **Operations:**
        - Create new strategies
        - List user strategies
        - Get strategy details
        - Update strategy parameters
        - Delete strategies
        """,
    },
    {
        "name": "📊 Backtests",
        "description": """
        Backtest execution and results retrieval endpoints.
        
        **Features:**
        - Run backtests with custom parameters
        - Retrieve backtest results and metrics
        - View equity curves and trade history
        - Compare multiple backtest runs
        
        **Metrics Calculated:**
        - ROI (Return on Investment)
        - Sharpe Ratio (risk-adjusted returns)
        - Maximum Drawdown
        - Win Rate
        - Profit Factor
        - Trade Statistics (avg, best, worst)
        """,
    },
    {
        "name": "📈 Market Data",
        "description": """
        Market data endpoints for accessing OHLCV data and indicators.
        
        **Data Available:**
        - Historical OHLCV data
        - Technical indicators (MA, RSI, MACD, etc)
        - Volume analysis
        """,
    },
]

# OpenAPI examples for request/response bodies
EXAMPLES = {
    "backtest_request": {
        "description": "Example backtest request",
        "value": {
            "strategy_id": 1,
            "symbol": "AAPL",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "initial_capital": 10000,
            "commission": 0.001,
            "slippage": 0.0005
        }
    },
    "backtest_result": {
        "description": "Example backtest result",
        "value": {
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
    },
    "strategy_request": {
        "description": "Example strategy creation request",
        "value": {
            "name": "Moving Average Crossover",
            "type": "mac",
            "parameters": {
                "fast_period": 10,
                "slow_period": 20
            },
            "description": "Classic MA crossover strategy"
        }
    },
    "strategy_response": {
        "description": "Example strategy response",
        "value": {
            "id": 1,
            "user_id": 1,
            "name": "Moving Average Crossover",
            "type": "mac",
            "parameters": {
                "fast_period": 10,
                "slow_period": 20
            },
            "description": "Classic MA crossover strategy",
            "created_at": "2024-02-16T10:00:00Z",
            "updated_at": "2024-02-16T10:00:00Z"
        }
    },
    "error_response": {
        "description": "Example error response",
        "value": {
            "detail": "Strategy not found",
            "status": 404,
            "timestamp": "2024-02-16T10:30:00Z"
        }
    }
}

# OpenAPI security schemes
SECURITY_SCHEMES = {
    "Bearer": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT token for authentication"
    }
}

# Common HTTP status codes and descriptions
HTTP_RESPONSES = {
    200: {"description": "Request successful"},
    201: {"description": "Resource created successfully"},
    400: {"description": "Bad request - Invalid parameters"},
    401: {"description": "Unauthorized - Missing or invalid token"},
    403: {"description": "Forbidden - Insufficient permissions"},
    404: {"description": "Not found - Resource does not exist"},
    422: {"description": "Unprocessable Entity - Validation error"},
    500: {"description": "Internal Server Error"},
}

# API response models documentation
RESPONSE_DESCRIPTIONS = {
    "backtest": {
        "status": "integer",
        "status_description": "HTTP status code",
        "data": {
            "id": "Backtest result ID",
            "strategy_id": "Associated strategy ID",
            "user_id": "User who ran the backtest",
            "total_return": "Absolute return amount (in currency)",
            "roi": "Return on Investment percentage",
            "sharpe_ratio": "Risk-adjusted return metric",
            "max_drawdown": "Maximum peak-to-trough decline percentage",
            "win_rate": "Percentage of profitable trades",
            "profit_factor": "Total profit / Total loss ratio",
            "total_trades": "Number of trades executed",
            "winning_trades": "Number of profitable trades",
            "losing_trades": "Number of losing trades",
            "average_trade": "Average profit/loss per trade",
            "best_trade": "Best single trade profit",
            "worst_trade": "Worst single trade loss",
            "trades": "Detailed trade history",
            "equity_curve": "Equity value over time",
        }
    },
    "strategy": {
        "id": "Strategy ID",
        "user_id": "User who created the strategy",
        "name": "Strategy name",
        "type": "Strategy type (mac, rsi, macd)",
        "parameters": "Strategy-specific parameters",
        "description": "Strategy description",
        "created_at": "Creation timestamp",
        "updated_at": "Last update timestamp",
    }
}
