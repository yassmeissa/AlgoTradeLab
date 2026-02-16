# CONTRIBUTING.md

## Guide de Contribution

Merci de votre intérêt pour contribuer à AlgoTrade Lab !

## Processus de Contribution

### 1. Fork & Clone

```bash
git clone https://github.com/yourusername/algotrade-lab.git
cd algotrade-lab/backend
```

### 2. Créer une branche

```bash
git checkout -b feature/votre-feature
# ou
git checkout -b bugfix/votre-bugfix
```

### 3. Développement

```bash
# Créer un venv
python -m venv venv
source venv/bin/activate

# Installer deps
pip install -r requirements.txt

# Développer...
# Exécuter les tests
pytest
```

### 4. Commit & Push

```bash
git add .
git commit -m "feat: description courte de votre changement"
git push origin feature/votre-feature
```

### 5. Pull Request

Créer une PR avec :
- Description claire
- Tests ajoutés
- Documentation mise à jour

## Normes de Code

### Style
- Suivre PEP 8
- Utiliser type hints
- Docstrings pour toutes les fonctions

```python
def calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.02) -> float:
    """Calculate Sharpe Ratio.
    
    Args:
        returns: Array of returns
        risk_free_rate: Risk-free rate (default: 2%)
    
    Returns:
        Sharpe ratio value
    """
    pass
```

### Tests
- Minimum 80% coverage
- Tests pour nouvelles features
- Tests pour bug fixes

```python
def test_moving_average():
    """Test moving average calculation"""
    data = pd.Series([1, 2, 3, 4, 5])
    result = moving_average(data, 2)
    expected = pd.Series([np.nan, 1.5, 2.5, 3.5, 4.5])
    pd.testing.assert_series_equal(result, expected)
```

## Types de Contributions

### 1. Nouvelles Stratégies

```python
# app/backtesting/strategies/votre_strategy.py
from app.backtesting.strategies.base_strategy import BaseStrategy

class VotreStrategy(BaseStrategy):
    def __init__(self, parameters):
        super().__init__("Votre Strategy", parameters)
    
    def generate_signals(self, data):
        # Implémentation
        return data
```

### 2. Nouveaux Indicateurs

```python
# Ajouter à app/backtesting/indicators/indicators.py
@staticmethod
def votre_indicateur(data, period=14):
    """Description."""
    return data.rolling(period).mean()
```

### 3. Corrections de Bugs

1. Créer une issue
2. Créer un test reproduisant le bug
3. Fixer le bug
4. Vérifier que tous les tests passent

### 4. Documentation

- README.md updates
- Code comments
- Docstrings
- API documentation

## Checklist avant PR

- [ ] Code suit PEP 8
- [ ] Tests écrits et passent
- [ ] Documentation mise à jour
- [ ] Pas de breaking changes
- [ ] Commit messages clairs
- [ ] Branch up-to-date avec main

## Questions ?

Créer une issue ou contacter : support@algotrade-lab.com
