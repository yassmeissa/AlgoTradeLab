"""Backtest routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Header, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from datetime import datetime
from app.db.database import get_db
from app.schemas.backtest import BacktestRequest, BacktestResultResponse
from app.services.backtest_service import BacktestService
from app.services.strategy_service import StrategyService
from app.services.user_service import UserService
from app.core.security import decode_token

router = APIRouter(prefix="/api/backtests", tags=["backtests"])


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


@router.post("/run", response_model=BacktestResultResponse)
def run_backtest(
    request: BacktestRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Run a backtest"""
    
    # Get strategy
    strategy = StrategyService.get_strategy(db, request.strategy_id, user_id)
    
    # For now, generate sample market data
    # In production, this would fetch real data from a data provider
    dates = pd.date_range(request.start_date, request.end_date, freq='D')
    market_data = pd.DataFrame({
        'open': [100 + i * 0.5 for i in range(len(dates))],
        'high': [102 + i * 0.5 for i in range(len(dates))],
        'low': [99 + i * 0.5 for i in range(len(dates))],
        'close': [101 + i * 0.5 for i in range(len(dates))],
        'volume': [1000000] * len(dates)
    }, index=dates)
    
    # Run backtest
    result = BacktestService.run_backtest(db, strategy, market_data)
    
    import json
    result_dict = result.__dict__.copy()
    result_dict["trades"] = json.loads(result.trades) if result.trades else []
    
    return result_dict


@router.get("/{result_id}", response_model=BacktestResultResponse)
def get_backtest_result(
    result_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get a backtest result"""
    result = BacktestService.get_backtest_result(db, result_id, user_id)
    
    import json
    result_dict = result.__dict__.copy()
    result_dict["trades"] = json.loads(result.trades) if result.trades else []
    
    return result_dict


@router.get("/strategy/{strategy_id}", response_model=List[BacktestResultResponse])
def list_backtest_results(
    strategy_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """List backtest results for a strategy"""
    results = BacktestService.list_backtest_results(db, strategy_id, user_id)
    
    import json
    result_list = []
    for result in results:
        result_dict = result.__dict__.copy()
        result_dict["trades"] = json.loads(result.trades) if result.trades else []
        result_list.append(result_dict)
    
    return result_list
