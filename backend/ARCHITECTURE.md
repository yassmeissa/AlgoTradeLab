# ARCHITECTURE.md - AlgoTrade Lab Backend Architecture

## Vue d'ensemble

AlgoTrade Lab est construit avec une architecture modulaire en couches, permettant séparation des responsabilités et facilité de maintenance.

```
┌─────────────────────────────────────────────────────┐
│           FastAPI HTTP Layer                         │
│  ┌─────────────────────────────────────────────────┐ │
│  │    API Routes (auth, strategies, backtests)    │ │
│  └─────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│          WebSocket Layer                             │
│  ┌─────────────────────────────────────────────────┐ │
│  │   Real-time Communication (ConnectionManager)   │ │
│  └─────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│         Business Logic Layer (Services)              │
│  ┌────────────┬──────────────┬──────────────────┐   │
│  │   User     │  Strategy    │    Backtest      │   │
│  │  Service   │  Service     │    Service       │   │
│  └────────────┴──────────────┴──────────────────┘   │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│    Core Logic Layer (Engine, Strategies, ML)         │
│  ┌──────────────┬─────────────┬──────────────────┐   │
│  │ Backtest     │ Strategies  │  ML Predictor    │   │
│  │ Engine       │ (Various)   │  (XGBoost, RF)   │   │
│  ├──────────────┼─────────────┼──────────────────┤   │
│  │ Indicators   │  Base       │  Feature Eng.    │   │
│  │ (Technical)  │  Strategy   │                  │   │
│  └──────────────┴─────────────┴──────────────────┘   │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│    Data Access Layer (ORM + Database)                │
│  ┌────────────────────────────────────────────────┐  │
│  │  SQLAlchemy Models (User, Strategy, Results)  │  │
│  ├────────────────────────────────────────────────┤  │
│  │  PostgreSQL Database                          │  │
│  │  - users table                                │  │
│  │  - strategies table                           │  │
│  │  - backtest_results table                     │  │
│  │  - market_data table                          │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│    External Services                                 │
│  ┌───────────────┬────────────────┬──────────────┐  │
│  │  PostgreSQL   │    Redis       │  Data APIs   │  │
│  │  (Persist.)   │    (Cache)     │  (External)  │  │
│  └───────────────┴────────────────┴──────────────┘  │
└──────────────────────────────────────────────────────┘
```

## Composants Clés

### 1. API Layer (`app/api/routes/`)

**Responsabilité**: Traiter les requêtes HTTP, valider les entrées, retourner les réponses.

**Fichiers**:
- `auth.py` - Authentification (register, login)
- `strategies.py` - CRUD stratégies
- `backtests.py` - Exécution et consultation backtests

**Stack**: FastAPI, Pydantic, FastAPI Dependencies

### 2. Service Layer (`app/services/`)

**Responsabilité**: Logique métier, orchestration des opérations.

**Fichiers**:
- `user_service.py` - Gestion utilisateurs
- `strategy_service.py` - CRUD stratégies
- `backtest_service.py` - Orchestration backtesting

**Pattern**: Service Pattern avec stateless functions

### 3. Core Engine (`app/backtesting/`)

**Responsabilité**: Simulation de trading, calcul de performances.

**Sous-modules**:

#### 3.1 Backtest Engine (`backtesting/engine/`)
```python
BacktestEngine:
  - run_backtest(data, strategy) → BacktestMetrics
  - _execute_trades(signals) → equity_curve
  - _calculate_metrics(equity, data) → metrics
```

**Algorithme de base**:
1. Générer signaux stratégie
2. Parcourir chaque candle
3. Exécuter trades sur signaux
4. Calculer equity à chaque étape
5. Retourner métriques de performance

#### 3.2 Strategies (`backtesting/strategies/`)

Base class `BaseStrategy`:
```python
class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(data) → DataFrame
```

Implémentations:
- `MovingAverageCrossoverStrategy` - MA crossover
- `RSIStrategy` - Oversold/Overbought
- `MACDStrategy` - MACD crossover

#### 3.3 Indicators (`backtesting/indicators/`)

`TechnicalIndicators` class:
- `moving_average(data, period)`
- `exponential_moving_average(data, period)`
- `rsi(data, period)`
- `macd(data, fast, slow, signal)`
- `bollinger_bands(data, period)`
- `atr(high, low, close, period)`
- `stochastic(high, low, close)`
- `adx(high, low, close)`

### 4. Machine Learning (`app/ml/`)

**MLPredictor**:
- `prepare_features(data)` - Feature engineering
- `create_labels(data, lookahead)` - Label generation
- `train(data)` - Model training
- `predict(data)` → trading signals
- `get_feature_importance()` - Feature analysis

**Modèles**:
- Logistic Regression
- Random Forest
- XGBoost

### 5. Data Access Layer (`app/db/`)

**SQLAlchemy ORM**:

```python
User
├── id (PK)
├── email (UNIQUE)
├── username (UNIQUE)
├── hashed_password
├── full_name
├── is_active
└── strategies (FK)

Strategy
├── id (PK)
├── user_id (FK)
├── name
├── description
├── strategy_type
├── parameters (JSON)
├── symbol
├── initial_capital
├── use_ml
└── backtest_results (FK)

BacktestResult
├── id (PK)
├── strategy_id (FK)
├── start_date
├── end_date
├── [Metrics...]
├── trades (JSON)
├── equity_curve (JSON)
└── status

MarketData
├── id (PK)
├── symbol
├── timestamp
├── open, high, low, close
└── volume
```

### 6. Schema/DTO Layer (`app/schemas/`)

**Pydantic Models** pour validation et sérialisation:
- `UserCreate`, `UserResponse`, `TokenResponse`
- `StrategyCreate`, `StrategyUpdate`, `StrategyResponse`
- `BacktestRequest`, `BacktestResultResponse`

### 7. Security (`app/core/security.py`)

- JWT token generation/validation
- Password hashing (bcrypt)
- Token expiration

### 8. Configuration (`app/core/config.py`)

- Settings management
- Environment variables
- Database URL, API keys, etc.

### 9. WebSocket (`app/websocket/`)

- `ConnectionManager` - Gestion connections
- `handlers.py` - Event handlers

## Flux de Données

### Register User
```
1. POST /auth/register
   ↓
2. UserCreate schema validation
   ↓
3. UserService.create_user()
   ├─ Check email/username uniqueness
   ├─ Hash password
   └─ Create User record
   ↓
4. Return UserResponse
```

### Create Strategy
```
1. POST /strategies
   ├─ Get user_id from JWT token
   ↓
2. StrategyCreate schema validation
   ↓
3. StrategyService.create_strategy()
   ├─ Serialize parameters to JSON
   └─ Create Strategy record
   ↓
4. Return StrategyResponse
```

### Run Backtest
```
1. POST /backtests/run
   ├─ Get user_id from JWT token
   ├─ Get Strategy record
   ↓
2. Load market data (from CSV, API, or generate)
   ↓
3. BacktestService.run_backtest()
   ├─ Parse strategy parameters
   ├─ Instantiate strategy class
   ├─ Create BacktestEngine
   ↓
4. BacktestEngine.run_backtest()
   ├─ strategy.generate_signals(data)
   ├─ Execute trades based on signals
   ├─ Calculate equity curve
   ├─ Calculate metrics
   └─ Return (metrics, details)
   ↓
5. Store BacktestResult in database
   ↓
6. Return BacktestResultResponse
```

## Patterns & Best Practices

### 1. Dependency Injection
```python
@router.post("/strategies/")
def create_strategy(
    strategy_data: StrategyCreate,
    user_id: int = Depends(get_current_user_id),  # Injected
    db: Session = Depends(get_db)                 # Injected
):
    pass
```

### 2. Repository Pattern
Services abstraient l'accès aux données:
```python
StrategyService.create_strategy(db, user_data)
StrategyService.get_strategy(db, strategy_id)
```

### 3. Factory Pattern
Strategies dynamiques:
```python
strategy_class = BacktestService.get_strategy_class(strategy_type)
strategy = strategy_class(parameters)
```

### 4. Strategy Pattern
Strategies pluggables:
```python
class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(self, data):
        pass
```

### 5. Async Operations
WebSocket communication asynchrone:
```python
async def broadcast(room_id, message):
    for connection in self.active_connections[room_id]:
        await connection.send_json(message)
```

## Scalabilité

### Optimisations Actuelles
- NumPy/Pandas pour calculs vectorisés
- Index PostgreSQL sur symbol/timestamp
- Lazy loading résultats
- JSON storage pour données flexibles

### Optimisations Futures
- Backtesting parallèle (multiprocessing)
- Redis caching pour données fréquentes
- Time-series database (InfluxDB)
- Event streaming (Kafka)
- Distributed backtesting
- WebSocket pub/sub (Redis)

## Déploiement

### Docker Compose
- PostgreSQL pour données persistantes
- Redis pour caching
- Backend API container
- Orchestration via docker-compose.yml

### Kubernetes (Future)
- Deployment pour API
- StatefulSet pour DB
- ConfigMap pour configuration
- Secrets pour credentials

## Monitoring & Observabilité

### Logs
- Centralized logging avec Python logging
- Format: timestamp, level, module, message

### Metrics (Future)
- Prometheus pour métriques
- Grafana pour dashboards
- Sentry pour error tracking

### Health Checks
- `/health` endpoint
- DB connectivity checks
- Cache connectivity checks

## Testing

### Unit Tests
- Test indicators
- Test strategies
- Test backtest engine
- Test services

### Integration Tests
- Test API endpoints
- Test database operations
- Test full backtest flow

### Fixtures
- Sample OHLCV data
- Test strategies
- Database fixtures
