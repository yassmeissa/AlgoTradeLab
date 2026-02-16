# README.md - Backend AlgoTrade Lab

## Description

Backend FastAPI pour la plateforme AlgoTrade Lab - Plateforme de Simulation et d'Analyse de Trading Algorithmique.

## Architecture

```
backend/
├── app/
│   ├── api/                      # Routes API FastAPI
│   │   └── routes/
│   │       ├── auth.py          # Authentification (Register/Login)
│   │       ├── strategies.py    # Gestion des stratégies
│   │       └── backtests.py     # Exécution et résultats de backtests
│   ├── backtesting/             # Moteur de backtesting
│   │   ├── engine/
│   │   │   └── backtest.py      # Moteur de calcul principal
│   │   ├── indicators/
│   │   │   └── indicators.py    # Indicateurs techniques
│   │   └── strategies/
│   │       ├── base_strategy.py # Classe de base
│   │       ├── moving_average_crossover.py
│   │       ├── rsi_strategy.py
│   │       └── macd_strategy.py
│   ├── core/                     # Configuration et utilitaires
│   │   ├── config.py            # Paramètres application
│   │   ├── security.py          # JWT, hachage passwords
│   │   └── logger.py            # Logging
│   ├── db/                       # Base de données
│   │   └── database.py          # SQLAlchemy setup
│   ├── models/                   # Modèles ORM
│   │   ├── user.py
│   │   ├── strategy.py
│   │   ├── backtest_result.py
│   │   └── market_data.py
│   ├── schemas/                  # Schémas Pydantic
│   │   ├── user.py
│   │   ├── strategy.py
│   │   └── backtest.py
│   ├── services/                 # Logique métier
│   │   ├── user_service.py
│   │   ├── strategy_service.py
│   │   └── backtest_service.py
│   ├── ml/                       # Machine Learning
│   │   └── ml_predictor.py      # Prédictions avec ML
│   └── websocket/                # Communication temps réel
│       ├── connection_manager.py
│       └── handlers.py
├── tests/                        # Tests unitaires
├── main.py                       # Point d'entrée
├── requirements.txt              # Dépendances Python
├── Dockerfile                    # Conteneurisation
├── docker-compose.yml            # Orchestration
└── .env.example                  # Variables d'environnement

```

## Fonctionnalités

### 1. Authentification
- Inscription / Connexion utilisateurs
- JWT tokens
- Hash sécurisé des mots de passe

### 2. Gestion des Stratégies
- CRUD complet pour les stratégies
- Support de multiples types (MA Crossover, RSI, MACD)
- Paramètres configurables

### 3. Moteur de Backtesting
- Simulation d'exécution de trades
- Calcul de métriques de performance
- Support des commissions et slippage

### 4. Indicateurs Techniques
- Moyennes Mobiles (SMA, EMA)
- RSI, MACD, Bandes de Bollinger
- ATR, Stochastique, ADX

### 5. Machine Learning
- Prédictions de signaux avec Logistic Regression, Random Forest, XGBoost
- Comparaison stratégie classique vs ML

### 6. Communication Temps Réel
- WebSockets pour mises à jour en direct
- Broadcast de signaux de trading

## Installation

### Avec Docker Compose (Recommandé)

```bash
cd backend
docker-compose up -d
```

Cela lancera :
- PostgreSQL (port 5432)
- Redis (port 6379)
- Backend FastAPI (port 8000)

### Installation locale

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# Lancer le serveur
uvicorn main:app --reload
```

## Configuration

Éditer le fichier `.env` :

```env
DATABASE_URL=postgresql://user:password@localhost:5432/algotrade_db
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ENVIRONMENT=development
```

## API Endpoints

### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `GET /api/auth/me` - Profil utilisateur

### Stratégies
- `POST /api/strategies/` - Créer stratégie
- `GET /api/strategies/` - Lister stratégies
- `GET /api/strategies/{id}` - Détails stratégie
- `PUT /api/strategies/{id}` - Modifier stratégie
- `DELETE /api/strategies/{id}` - Supprimer stratégie

### Backtests
- `POST /api/backtests/run` - Lancer backtest
- `GET /api/backtests/{id}` - Résultat backtest
- `GET /api/backtests/strategy/{strategy_id}` - Historique backtests

## Documentation API

Après démarrage du serveur :
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Tests

```bash
# Lancer les tests
pytest

# Avec couverture
pytest --cov=app tests/
```

## Stratégies Disponibles

### 1. Moving Average Crossover
Paramètres :
- `fast_period`: Période MA rapide (défaut: 10)
- `slow_period`: Période MA lente (défaut: 20)

### 2. RSI (Relative Strength Index)
Paramètres :
- `rsi_period`: Période RSI (défaut: 14)
- `oversold_threshold`: Seuil de survente (défaut: 30)
- `overbought_threshold`: Seuil de surache (défaut: 70)

### 3. MACD (Moving Average Convergence Divergence)
Paramètres :
- `fast_period`: Période EMA rapide (défaut: 12)
- `slow_period`: Période EMA lente (défaut: 26)
- `signal_period`: Période signal (défaut: 9)

## Indicateurs Techniques

### Volatilité
- Bollinger Bands
- ATR (Average True Range)

### Momentum
- RSI
- Stochastique

### Tendance
- MACD
- ADX

### Volume
- OBV (On-Balance Volume)

## Métriques de Performance

- **ROI** : Return on Investment
- **Sharpe Ratio** : Performance ajustée au risque
- **Maximum Drawdown** : Perte maximale
- **Win Rate** : Pourcentage de trades gagnants
- **Profit Factor** : Profit total / Perte totale

## Machine Learning

### Modèles Disponibles
1. Logistic Regression
2. Random Forest
3. XGBoost

### Features
- Indicateurs techniques
- Variations de prix
- Variations de volume

## WebSockets

Connexion temps réel pour :
- Mises à jour de backtests
- Signaux de trading en direct
- Keep-alive (ping/pong)

```
ws://localhost:8000/ws/{room_id}
```

## Performance

- Backtesting optimisé avec NumPy/Pandas
- Caching Redis pour données fréquentes
- Lazy loading des résultats
- Index PostgreSQL sur symboles/dates

## Sécurité

- JWT authentication
- CORS configuré
- Password hashing (bcrypt)
- SQL Injection prevention (ORM)
- HTTPS ready (prod)

## Développement

### Ajouter une nouvelle stratégie

```python
from app.backtesting.strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self, parameters):
        super().__init__("My Strategy", parameters)
    
    def generate_signals(self, data):
        # Implémentation
        data["signal"] = ...
        return data
```

### Ajouter un nouvel indicateur

```python
from app.backtesting.indicators.indicators import TechnicalIndicators

@staticmethod
def my_indicator(data, period=14):
    return data.rolling(window=period).mean()
```

## Troubleshooting

### Erreur de connexion DB
- Vérifier DATABASE_URL
- S'assurer que PostgreSQL est démarré

### Erreur d'import
- Installer les dépendances: `pip install -r requirements.txt`
- Vérifier le PYTHONPATH

### Tests échouent
- Vérifier la base de données test
- `pytest -v` pour détails

## Prochaines Améliorations

- [ ] Support données en temps réel (WebSocket)
- [ ] Optimisation portefeuille multi-stratégie
- [ ] Backtesting parallèle
- [ ] Export résultats (PDF, Excel)
- [ ] API données externes (Alpha Vantage, etc.)
- [ ] Cache distribué Redis
- [ ] Logging centralisé (ELK)
- [ ] Monitoring (Prometheus/Grafana)

## Licence

MIT

## Contact

Pour questions/support : support@algotrade-lab.com
