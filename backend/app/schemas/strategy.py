"""Strategy schemas"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
import json


class StrategyCreate(BaseModel):
    """Strategy creation schema"""
    name: str
    description: Optional[str] = None
    strategy_type: str  # moving_average_crossover, rsi, macd, etc.
    parameters: Dict[str, Any]  # Strategy-specific parameters
    symbol: str
    initial_capital: float = 10000.0
    use_ml: bool = False


class StrategyUpdate(BaseModel):
    """Strategy update schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    initial_capital: Optional[float] = None
    use_ml: Optional[bool] = None


class StrategyResponse(BaseModel):
    """Strategy response schema"""
    id: int
    name: str
    description: Optional[str]
    strategy_type: str
    parameters: Dict[str, Any]
    symbol: str
    initial_capital: float
    use_ml: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
    
    @property
    def parameters_dict(self) -> Dict[str, Any]:
        """Parse parameters if they're JSON string"""
        if isinstance(self.parameters, str):
            return json.loads(self.parameters)
        return self.parameters
