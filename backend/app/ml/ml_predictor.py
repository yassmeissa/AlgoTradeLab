"""ML-based trading signal predictor"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from app.backtesting.indicators.indicators import TechnicalIndicators


class MLPredictor:
    """Machine Learning predictor for trading signals"""
    
    def __init__(self, model_type: str = "logistic_regression"):
        """
        Initialize ML predictor
        
        Args:
            model_type: Type of model - "logistic_regression", "random_forest", "xgboost"
        """
        self.model_type = model_type
        self.model = self._get_model()
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def _get_model(self):
        """Get model based on type"""
        if self.model_type == "logistic_regression":
            return LogisticRegression(random_state=42, max_iter=1000)
        elif self.model_type == "random_forest":
            return RandomForestClassifier(n_estimators=100, random_state=42)
        elif self.model_type == "xgboost":
            return XGBClassifier(n_estimators=100, random_state=42)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for ML model"""
        features = data.copy()
        
        # Technical indicators as features
        features["sma_10"] = TechnicalIndicators.moving_average(data["close"], 10)
        features["sma_20"] = TechnicalIndicators.moving_average(data["close"], 20)
        features["rsi"] = TechnicalIndicators.rsi(data["close"], 14)
        
        macd, signal, _ = TechnicalIndicators.macd(data["close"])
        features["macd"] = macd
        features["macd_signal"] = signal
        
        upper, mid, lower = TechnicalIndicators.bollinger_bands(data["close"])
        features["bb_upper"] = upper
        features["bb_lower"] = lower
        
        features["atr"] = TechnicalIndicators.atr(data["high"], data["low"], data["close"])
        
        # Price features
        features["price_change"] = data["close"].pct_change()
        features["volume_change"] = data["volume"].pct_change()
        
        # Remove NaN values
        features = features.dropna()
        
        return features
    
    def create_labels(self, data: pd.DataFrame, lookahead: int = 5) -> np.ndarray:
        """Create labels for training (1=UP, 0=DOWN)"""
        labels = np.zeros(len(data))
        
        for i in range(len(data) - lookahead):
            future_price = data["close"].iloc[i + lookahead]
            current_price = data["close"].iloc[i]
            
            if future_price > current_price:
                labels[i] = 1  # UP
            else:
                labels[i] = 0  # DOWN
        
        return labels
    
    def train(self, data: pd.DataFrame, lookahead: int = 5):
        """Train the ML model"""
        # Prepare features
        features = self.prepare_features(data)
        
        # Create labels
        labels = self.create_labels(data, lookahead)
        labels = labels[:len(features)]
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(features.drop(["open", "high", "low", "close", "volume"], axis=1, errors="ignore"))
        
        # Train model
        self.model.fit(X_scaled, labels)
        self.is_trained = True
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """Predict trading signals"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Prepare features
        features = self.prepare_features(data)
        
        # Normalize features
        X_scaled = self.scaler.transform(features.drop(["open", "high", "low", "close", "volume"], axis=1, errors="ignore"))
        
        # Get predictions and probabilities
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        
        # Create result dataframe
        result = features.copy()
        result["ml_signal"] = predictions
        result["confidence"] = probabilities[:, 1]
        
        # Convert to trading signals (1=BUY, -1=SELL, 0=HOLD)
        result["signal"] = 0
        result.loc[result["ml_signal"] == 1, "signal"] = 1  # BUY
        result.loc[result["ml_signal"] == 0, "signal"] = -1  # SELL
        
        return result
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance (if available for model)"""
        if hasattr(self.model, "feature_importances_"):
            feature_names = [
                "sma_10", "sma_20", "rsi", "macd", "macd_signal",
                "bb_upper", "bb_lower", "atr", "price_change", "volume_change"
            ]
            importances = dict(zip(feature_names, self.model.feature_importances_))
            return sorted(importances.items(), key=lambda x: x[1], reverse=True)
        return {}
