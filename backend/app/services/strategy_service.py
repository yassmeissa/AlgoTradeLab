"""Strategy service"""

from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from app.models.strategy import Strategy
from app.schemas.strategy import StrategyCreate, StrategyUpdate
from fastapi import HTTPException, status


class StrategyService:
    """Strategy business logic"""
    
    @staticmethod
    def create_strategy(db: Session, user_id: int, strategy_data: StrategyCreate) -> Strategy:
        """Create a new strategy"""
        strategy = Strategy(
            user_id=user_id,
            name=strategy_data.name,
            description=strategy_data.description,
            strategy_type=strategy_data.strategy_type,
            parameters=json.dumps(strategy_data.parameters),
            symbol=strategy_data.symbol,
            initial_capital=strategy_data.initial_capital,
            use_ml=strategy_data.use_ml
        )
        
        db.add(strategy)
        db.commit()
        db.refresh(strategy)
        
        return strategy
    
    @staticmethod
    def get_strategy(db: Session, strategy_id: int, user_id: int) -> Strategy:
        """Get strategy by ID"""
        strategy = db.query(Strategy).filter(
            Strategy.id == strategy_id,
            Strategy.user_id == user_id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Strategy not found"
            )
        
        return strategy
    
    @staticmethod
    def list_strategies(db: Session, user_id: int) -> List[Strategy]:
        """List all strategies for a user"""
        return db.query(Strategy).filter(Strategy.user_id == user_id).all()
    
    @staticmethod
    def update_strategy(db: Session, strategy_id: int, user_id: int, strategy_data: StrategyUpdate) -> Strategy:
        """Update a strategy"""
        strategy = StrategyService.get_strategy(db, strategy_id, user_id)
        
        update_data = strategy_data.dict(exclude_unset=True)
        
        if "parameters" in update_data and update_data["parameters"]:
            update_data["parameters"] = json.dumps(update_data["parameters"])
        
        for key, value in update_data.items():
            setattr(strategy, key, value)
        
        db.add(strategy)
        db.commit()
        db.refresh(strategy)
        
        return strategy
    
    @staticmethod
    def delete_strategy(db: Session, strategy_id: int, user_id: int):
        """Delete a strategy"""
        strategy = StrategyService.get_strategy(db, strategy_id, user_id)
        db.delete(strategy)
        db.commit()
