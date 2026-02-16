# API DOCUMENTATION

## Authentication Endpoints

### Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "secure_password",
  "full_name": "John Doe"
}

Response 200:
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T10:00:00Z"
}
```

### Login User
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}

Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Get Current User
```
GET /api/auth/me
Authorization: Bearer {token}

Response 200:
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T10:00:00Z"
}
```

## Strategy Endpoints

### Create Strategy
```
POST /api/strategies/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "MA Crossover Strategy",
  "description": "Moving Average Crossover with fast=10, slow=20",
  "strategy_type": "moving_average_crossover",
  "parameters": {
    "fast_period": 10,
    "slow_period": 20
  },
  "symbol": "AAPL",
  "initial_capital": 10000,
  "use_ml": false
}

Response 200:
{
  "id": 1,
  "name": "MA Crossover Strategy",
  "description": "...",
  "strategy_type": "moving_average_crossover",
  "parameters": {
    "fast_period": 10,
    "slow_period": 20
  },
  "symbol": "AAPL",
  "initial_capital": 10000,
  "use_ml": false,
  "is_active": true,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### List Strategies
```
GET /api/strategies/
Authorization: Bearer {token}

Response 200:
[
  {
    "id": 1,
    "name": "MA Crossover Strategy",
    ...
  },
  {
    "id": 2,
    "name": "RSI Strategy",
    ...
  }
]
```

### Get Strategy
```
GET /api/strategies/{strategy_id}
Authorization: Bearer {token}

Response 200:
{
  "id": 1,
  "name": "MA Crossover Strategy",
  ...
}
```

### Update Strategy
```
PUT /api/strategies/{strategy_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Updated Strategy Name",
  "initial_capital": 15000
}

Response 200:
{
  "id": 1,
  "name": "Updated Strategy Name",
  ...
}
```

### Delete Strategy
```
DELETE /api/strategies/{strategy_id}
Authorization: Bearer {token}

Response 200:
{
  "message": "Strategy deleted successfully"
}
```

## Backtest Endpoints

### Run Backtest
```
POST /api/backtests/run
Authorization: Bearer {token}
Content-Type: application/json

{
  "strategy_id": 1,
  "start_date": "2023-01-01T00:00:00Z",
  "end_date": "2023-12-31T23:59:59Z"
}

Response 200:
{
  "id": 1,
  "strategy_id": 1,
  "start_date": "2023-01-01T00:00:00Z",
  "end_date": "2023-12-31T23:59:59Z",
  "total_return": 2500.50,
  "roi": 25.05,
  "sharpe_ratio": 1.45,
  "max_drawdown": -8.32,
  "win_rate": 65.5,
  "profit_factor": 2.15,
  "total_trades": 45,
  "winning_trades": 30,
  "losing_trades": 15,
  "average_trade": 55.67,
  "best_trade": 450.00,
  "worst_trade": -150.00,
  "status": "completed",
  "trades": [
    {
      "entry_date": "2023-01-01T10:00:00Z",
      "exit_date": "2023-01-02T14:30:00Z",
      "entry_price": 150.00,
      "exit_price": 152.50,
      "quantity": 66,
      "side": "BUY",
      "pnl": 165.00,
      "pnl_percent": 1.67
    }
  ],
  "created_at": "2024-01-01T10:00:00Z"
}
```

### Get Backtest Result
```
GET /api/backtests/{result_id}
Authorization: Bearer {token}

Response 200:
{
  "id": 1,
  "strategy_id": 1,
  ...
}
```

### List Backtest Results for Strategy
```
GET /api/backtests/strategy/{strategy_id}
Authorization: Bearer {token}

Response 200:
[
  {
    "id": 1,
    "strategy_id": 1,
    ...
  },
  {
    "id": 2,
    "strategy_id": 1,
    ...
  }
]
```

## Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "status_code": 400,
  "message": "Invalid request parameters",
  "errors": ["strategy_type must be one of: ..."]
}
```

### 401 Unauthorized
```json
{
  "status": "error",
  "status_code": 401,
  "message": "Missing or invalid authorization header"
}
```

### 404 Not Found
```json
{
  "status": "error",
  "status_code": 404,
  "message": "Strategy not found"
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "status_code": 500,
  "message": "Internal server error",
  "errors": ["Error details..."]
}
```

## Rate Limiting

Not yet implemented. Will be added in future versions.

## Pagination

List endpoints support pagination:

```
GET /api/strategies/?page=1&page_size=20
```

Response includes pagination info:
```json
{
  "data": [...],
  "pagination": {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  }
}
```

## WebSocket

Connect to WebSocket for real-time updates:

```
ws://localhost:8000/ws/{room_id}
```

Send messages:
```json
{
  "type": "backtest_update",
  "data": {...}
}
```

Listen for messages:
```json
{
  "type": "backtest_update",
  "data": {...}
}
```

## Health Check

```
GET /health

Response 200:
{
  "status": "healthy"
}
```
