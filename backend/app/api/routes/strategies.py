"""Strategy routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.strategy import StrategyCreate, StrategyUpdate, StrategyResponse
from app.services.strategy_service import StrategyService
from app.services.user_service import UserService
from app.core.security import decode_token

router = APIRouter(prefix="/api/strategies", tags=["strategies"])


def get_current_user_id(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Get current user ID from token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = UserService.get_user_by_id(db, payload["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user.id


@router.post("/", response_model=StrategyResponse)
def create_strategy(
    strategy_data: StrategyCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new strategy"""
    strategy = StrategyService.create_strategy(db, user_id, strategy_data)
    
    # Parse parameters for response
    import json
    strategy_dict = strategy.__dict__.copy()
    strategy_dict["parameters"] = json.loads(strategy.parameters)
    
    return strategy_dict


@router.get("/", response_model=List[StrategyResponse])
def list_strategies(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """List all strategies for user"""
    strategies = StrategyService.list_strategies(db, user_id)
    
    import json
    result = []
    for strategy in strategies:
        strategy_dict = strategy.__dict__.copy()
        strategy_dict["parameters"] = json.loads(strategy.parameters)
        result.append(strategy_dict)
    
    return result


@router.get("/{strategy_id}", response_model=StrategyResponse)
def get_strategy(
    strategy_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get a specific strategy"""
    strategy = StrategyService.get_strategy(db, strategy_id, user_id)
    
    import json
    strategy_dict = strategy.__dict__.copy()
    strategy_dict["parameters"] = json.loads(strategy.parameters)
    
    return strategy_dict


@router.put("/{strategy_id}", response_model=StrategyResponse)
def update_strategy(
    strategy_id: int,
    strategy_data: StrategyUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update a strategy"""
    strategy = StrategyService.update_strategy(db, strategy_id, user_id, strategy_data)
    
    import json
    strategy_dict = strategy.__dict__.copy()
    strategy_dict["parameters"] = json.loads(strategy.parameters)
    
    return strategy_dict


@router.delete("/{strategy_id}")
def delete_strategy(
    strategy_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete a strategy"""
    StrategyService.delete_strategy(db, strategy_id, user_id)
    return {"message": "Strategy deleted successfully"}
