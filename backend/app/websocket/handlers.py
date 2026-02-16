"""WebSocket event handlers"""

from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.websocket.connection_manager import manager
import json


async def websocket_endpoint(websocket: WebSocket, room_id: str, db: Session = Depends(get_db)):
    """WebSocket endpoint handler"""
    
    await manager.connect(room_id, websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "backtest_update":
                # Broadcast backtest updates to all clients in the room
                await manager.broadcast(room_id, {
                    "type": "backtest_update",
                    "data": message.get("data")
                })
            
            elif message.get("type") == "trade_signal":
                # Broadcast trading signals
                await manager.broadcast(room_id, {
                    "type": "trade_signal",
                    "data": message.get("data")
                })
            
            elif message.get("type") == "ping":
                # Handle ping/pong for connection keep-alive
                await manager.send_personal(websocket, {"type": "pong"})
    
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
