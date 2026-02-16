"""WebSocket connection manager"""

from typing import List, Dict
from fastapi import WebSocket
import json


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, room_id: str, websocket: WebSocket):
        """Connect a WebSocket to a room"""
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
    
    def disconnect(self, room_id: str, websocket: WebSocket):
        """Disconnect a WebSocket from a room"""
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
    
    async def broadcast(self, room_id: str, message: Dict):
        """Broadcast a message to all connections in a room"""
        if room_id not in self.active_connections:
            return
        
        message_json = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections[room_id]:
            try:
                await connection.send_text(message_json)
            except Exception:
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(room_id, connection)
    
    async def send_personal(self, websocket: WebSocket, message: Dict):
        """Send a message to a specific connection"""
        try:
            await websocket.send_json(message)
        except Exception:
            pass


manager = ConnectionManager()
