"""Seed test data for different users"""

from sqlalchemy.orm import Session
from app.db.database import engine, SessionLocal, Base
from app.models.user import User
from app.models.strategy import Strategy
from app.models.backtest_result import BacktestResult
from app.core.security import hash_password
from datetime import datetime, timedelta
import json

def seed_database():
    """Create tables and seed with test data"""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("Database already seeded!")
            return
        
        # Create User 1: Alice (Tech-focused trader)
        user1 = User(
            username="alice",
            email="alice@example.com",
            hashed_password=hash_password("Alice@123"),
            full_name="Alice Johnson",
            is_active=True
        )
        db.add(user1)
        db.flush()
        
        # Create User 2: Bob (Conservative trader)
        user2 = User(
            username="bob",
            email="bob@example.com",
            hashed_password=hash_password("Bob@123"),
            full_name="Bob Smith",
            is_active=True
        )
        db.add(user2)
        db.flush()
        
        # Strategies for Alice (Tech trader)
        strategy1 = Strategy(
            user_id=user1.id,
            name="Tech Growth Strategy",
            description="MACD-based strategy for tech stocks (AAPL, MSFT, NVDA)",
            strategy_type="macd_strategy",
            parameters=json.dumps({
                "fast_period": 12,
                "slow_period": 26,
                "signal_period": 9,
                "symbols": ["AAPL", "MSFT", "NVDA"]
            }),
            symbol="AAPL",
            initial_capital=50000.0,
            is_active=True,
            use_ml=False
        )
        db.add(strategy1)
        db.flush()
        
        strategy2 = Strategy(
            user_id=user1.id,
            name="RSI Momentum",
            description="RSI-based momentum strategy for high-cap stocks",
            strategy_type="rsi_strategy",
            parameters=json.dumps({
                "period": 14,
                "overbought": 70,
                "oversold": 30,
                "symbols": ["MSFT", "GOOGL"]
            }),
            symbol="MSFT",
            initial_capital=30000.0,
            is_active=True,
            use_ml=False
        )
        db.add(strategy2)
        db.flush()
        
        # Strategies for Bob (Conservative trader)
        strategy3 = Strategy(
            user_id=user2.id,
            name="Moving Average Crossover",
            description="Classic MA crossover strategy for stable stocks",
            strategy_type="moving_average_crossover",
            parameters=json.dumps({
                "fast_ma": 20,
                "slow_ma": 50,
                "symbols": ["JNJ", "KO", "PG"]
            }),
            symbol="JNJ",
            initial_capital=25000.0,
            is_active=True,
            use_ml=False
        )
        db.add(strategy3)
        db.flush()
        
        strategy4 = Strategy(
            user_id=user2.id,
            name="Dividend Hunter",
            description="Conservative strategy for dividend-paying stocks",
            strategy_type="moving_average_crossover",
            parameters=json.dumps({
                "fast_ma": 50,
                "slow_ma": 200,
                "symbols": ["KO", "PG", "VZ"]
            }),
            symbol="KO",
            initial_capital=20000.0,
            is_active=False,
            use_ml=False
        )
        db.add(strategy4)
        db.flush()
        
        # Backtest results for Alice's strategy 1
        backtest1 = BacktestResult(
            strategy_id=strategy1.id,
            start_date=datetime.utcnow() - timedelta(days=365),
            end_date=datetime.utcnow(),
            total_return=45.8,
            roi=45.8,
            sharpe_ratio=1.85,
            max_drawdown=-12.5,
            win_rate=58.3,
            profit_factor=2.15,
            total_trades=142,
            winning_trades=83,
            losing_trades=59,
            average_trade=322.50,
            best_trade=2850.0,
            worst_trade=-1200.0,
            status="completed",
            trades=json.dumps([
                {"date": "2026-01-15", "type": "BUY", "price": 150.25, "quantity": 100},
                {"date": "2026-01-16", "type": "SELL", "price": 152.75, "quantity": 100},
            ]),
            equity_curve=json.dumps([
                {"date": "2025-02-16", "value": 50000},
                {"date": "2025-08-16", "value": 58500},
                {"date": "2026-02-16", "value": 72900}
            ])
        )
        db.add(backtest1)
        db.flush()
        
        # Backtest results for Alice's strategy 2
        backtest2 = BacktestResult(
            strategy_id=strategy2.id,
            start_date=datetime.utcnow() - timedelta(days=180),
            end_date=datetime.utcnow(),
            total_return=28.5,
            roi=28.5,
            sharpe_ratio=1.42,
            max_drawdown=-8.3,
            win_rate=61.2,
            profit_factor=1.95,
            total_trades=98,
            winning_trades=60,
            losing_trades=38,
            average_trade=285.00,
            best_trade=1950.0,
            worst_trade=-850.0,
            status="completed",
            trades=json.dumps([]),
            equity_curve=json.dumps([
                {"date": "2025-09-16", "value": 30000},
                {"date": "2025-12-16", "value": 32100},
                {"date": "2026-02-16", "value": 38550}
            ])
        )
        db.add(backtest2)
        db.flush()
        
        # Backtest results for Bob's strategy 1
        backtest3 = BacktestResult(
            strategy_id=strategy3.id,
            start_date=datetime.utcnow() - timedelta(days=365),
            end_date=datetime.utcnow(),
            total_return=18.6,
            roi=18.6,
            sharpe_ratio=0.95,
            max_drawdown=-6.2,
            win_rate=55.1,
            profit_factor=1.58,
            total_trades=87,
            winning_trades=48,
            losing_trades=39,
            average_trade=213.79,
            best_trade=1200.0,
            worst_trade=-650.0,
            status="completed",
            trades=json.dumps([]),
            equity_curve=json.dumps([
                {"date": "2025-02-16", "value": 25000},
                {"date": "2025-08-16", "value": 26800},
                {"date": "2026-02-16", "value": 29650}
            ])
        )
        db.add(backtest3)
        db.flush()
        
        # Commit all changes
        db.commit()
        print("✅ Database seeded with test data!")
        print(f"   - User 1 (Alice): 2 strategies, 2 backtests")
        print(f"   - User 2 (Bob): 2 strategies, 1 backtest")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
