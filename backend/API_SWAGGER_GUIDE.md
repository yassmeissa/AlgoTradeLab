# 📚 AlgoTrade Lab API - Swagger/OpenAPI Documentation

## 🚀 Quick Start

FastAPI génère automatiquement une documentation interactive Swagger à:

```
📍 Swagger UI:  http://localhost:8000/docs
📍 ReDoc:       http://localhost:8000/redoc
📍 OpenAPI JSON: http://localhost:8000/openapi.json
```

## 🎯 Comment Utiliser la Documentation

### 1. **Accéder à Swagger UI**
```bash
# Démarrer le serveur
python run.py

# Ouvrir dans le navigateur
http://localhost:8000/docs
```

### 2. **Essayer une Requête**
- Cliquer sur un endpoint
- Cliquer sur "Try it out"
- Remplir les paramètres
- Cliquer "Execute"
- Voir la réponse

### 3. **Authentication**
- Obtenir un token via `/api/auth/login`
- Copier le token dans le bouton "Authorize"
- Utiliser le format: `Bearer <token>`

---

## 📊 API Endpoints

### 🔐 Authentication (`/api/auth/`)

#### `POST /api/auth/register`
**Créer un nouvel utilisateur**

```json
Request:
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "full_name": "John Doe"
}

Response (201):
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "created_at": "2024-02-16T10:00:00Z"
}
```

#### `POST /api/auth/login`
**Se connecter et obtenir un token JWT**

```json
Request:
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### `POST /api/auth/refresh`
**Rafraîchir le token JWT**

```json
Request Header:
Authorization: Bearer <expired_token>

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 🎯 Strategies (`/api/strategies/`)

#### `POST /api/strategies`
**Créer une nouvelle stratégie**

```json
Request:
{
  "name": "Moving Average Crossover",
  "type": "mac",
  "parameters": {
    "fast_period": 10,
    "slow_period": 20
  },
  "description": "Classic MA crossover strategy"
}

Response (201):
{
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
```

**Stratégies Supportées:**

1. **MAC (Moving Average Crossover)**
   ```json
   {
     "type": "mac",
     "parameters": {
       "fast_period": 10,
       "slow_period": 20
     }
   }
   ```

2. **RSI (Relative Strength Index)**
   ```json
   {
     "type": "rsi",
     "parameters": {
       "rsi_period": 14,
       "oversold_threshold": 30,
       "overbought_threshold": 70
     }
   }
   ```

3. **MACD (Moving Average Convergence Divergence)**
   ```json
   {
     "type": "macd",
     "parameters": {
       "fast_ema": 12,
       "slow_ema": 26,
       "signal_period": 9
     }
   }
   ```

#### `GET /api/strategies`
**Lister toutes les stratégies de l'utilisateur**

```
Query Parameters:
- skip: 0          (nombre de résultats à sauter)
- limit: 10        (max résultats à retourner)

Response (200):
[
  {
    "id": 1,
    "name": "Moving Average Crossover",
    "type": "mac",
    "parameters": {...},
    "created_at": "2024-02-16T10:00:00Z"
  },
  ...
]
```

#### `GET /api/strategies/{strategy_id}`
**Obtenir les détails d'une stratégie**

```
Response (200):
{
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
```

#### `PUT /api/strategies/{strategy_id}`
**Mettre à jour une stratégie**

```json
Request:
{
  "name": "Improved MA Crossover",
  "parameters": {
    "fast_period": 12,
    "slow_period": 25
  }
}

Response (200):
{
  "id": 1,
  "name": "Improved MA Crossover",
  "type": "mac",
  "parameters": {
    "fast_period": 12,
    "slow_period": 25
  },
  "updated_at": "2024-02-16T11:00:00Z"
}
```

#### `DELETE /api/strategies/{strategy_id}`
**Supprimer une stratégie**

```
Response (204):
No content
```

---

### 📊 Backtests (`/api/backtests/`)

#### `POST /api/backtests/run`
**Exécuter un backtest**

```json
Request:
{
  "strategy_id": 1,
  "symbol": "AAPL",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "initial_capital": 10000,
  "commission": 0.001,
  "slippage": 0.0005
}

Response (200):
{
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
  "trades": [
    {
      "entry_date": "2023-01-15",
      "entry_price": 150.25,
      "exit_date": "2023-02-20",
      "exit_price": 160.50,
      "quantity": 66,
      "side": "BUY",
      "pnl": 679.50,
      "pnl_percent": 6.83
    }
  ],
  "equity_curve": [10000, 10100, 10050, 10250, ...],
  "created_at": "2024-02-16T10:30:00Z"
}
```

#### `GET /api/backtests/{result_id}`
**Obtenir les résultats d'un backtest**

```
Response (200):
{
  "id": 1,
  "strategy_id": 1,
  "user_id": 1,
  "total_return": 875.50,
  "roi": 8.75,
  ...
}
```

#### `GET /api/backtests`
**Lister tous les backtests de l'utilisateur**

```
Query Parameters:
- skip: 0          (nombre de résultats à sauter)
- limit: 10        (max résultats à retourner)

Response (200):
[
  {
    "id": 1,
    "strategy_id": 1,
    "roi": 8.75,
    "total_return": 875.50,
    "win_rate": 62.5,
    "created_at": "2024-02-16T10:30:00Z"
  },
  ...
]
```

#### `DELETE /api/backtests/{result_id}`
**Supprimer un résultat de backtest**

```
Response (204):
No content
```

---

## 🔐 Authentication

### JWT Bearer Token

Tous les endpoints (sauf `/api/auth/register` et `/api/auth/login`) nécessitent un JWT token.

**Format du Header:**
```
Authorization: Bearer <token>
```

**Exemple avec curl:**
```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  http://localhost:8000/api/strategies
```

**Exemple avec Python:**
```python
import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(
  "http://localhost:8000/api/strategies",
  headers=headers
)
```

---

## 📈 Performance Metrics Explanation

### ROI (Return on Investment)
```
ROI = ((Final Value - Initial Capital) / Initial Capital) * 100
```

### Sharpe Ratio
```
Sharpe = (Average Return - Risk-Free Rate) / Std Dev of Returns * sqrt(252)

Higher is better (> 1.0 is good)
```

### Maximum Drawdown
```
Max Drawdown = (Lowest Point - Peak Before It) / Peak * 100

More negative means worse
```

### Win Rate
```
Win Rate = (Number of Winning Trades / Total Trades) * 100
```

### Profit Factor
```
Profit Factor = Total Profit / Total Loss

> 1.0 means profitable
> 2.0 means very profitable
```

---

## ⚠️ Common Errors

### 401 Unauthorized
```json
{
  "detail": "Invalid or missing authorization header",
  "status": 401
}
```
**Solution:** Inclure le token JWT dans le header Authorization

### 404 Not Found
```json
{
  "detail": "Strategy not found",
  "status": 404
}
```
**Solution:** Vérifier l'ID existe et appartient à l'utilisateur

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "initial_capital"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ],
  "status": 422
}
```
**Solution:** Vérifier les paramètres de la requête

---

## 🧪 Testing avec Swagger

### Workflow Complet

1. **Register User**
   ```
   POST /api/auth/register
   Body: {
     "email": "test@example.com",
     "password": "Test123456",
     "full_name": "Test User"
   }
   ```

2. **Login**
   ```
   POST /api/auth/login
   Body: {
     "email": "test@example.com",
     "password": "Test123456"
   }
   Copy: access_token
   ```

3. **Authorize**
   - Click "Authorize" button
   - Paste token: `Bearer <token>`
   - Click "Authorize"

4. **Create Strategy**
   ```
   POST /api/strategies
   Body: {
     "name": "MAC Strategy",
     "type": "mac",
     "parameters": {
       "fast_period": 10,
       "slow_period": 20
     }
   }
   Copy: id (strategy_id)
   ```

5. **Run Backtest**
   ```
   POST /api/backtests/run
   Body: {
     "strategy_id": 1,
     "symbol": "AAPL",
     "start_date": "2023-01-01",
     "end_date": "2023-12-31",
     "initial_capital": 10000
   }
   ```

6. **View Results**
   ```
   GET /api/backtests/{result_id}
   ```

---

## 🚀 Production Deployment

### Uvicorn Configuration
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```bash
docker build -t algotrade-api .
docker run -p 8000:8000 algotrade-api
```

### Access API
```
http://your-domain.com:8000/docs     # Swagger UI
http://your-domain.com:8000/redoc    # ReDoc
http://your-domain.com:8000/api/*    # API Endpoints
```

---

## 📚 References

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **OpenAPI Spec:** https://spec.openapis.org/
- **JWT.io:** https://jwt.io/
- **GitHub:** https://github.com/yassmeissa/AlgoTradeLab

---

**Version:** 2.1.0
**Last Updated:** 16 février 2026
**Status:** ✅ Production Ready
