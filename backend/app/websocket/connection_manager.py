from typing import Dict, List
from fastapi import WebSocket
import json
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        # Structure: {channel_id: {user_id: websocket}}
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, channel_id: int, user_id: int):
        """Connect a user to a channel"""
        await websocket.accept()
        
        if channel_id not in self.active_connections:
            self.active_connections[channel_id] = {}
        
        self.active_connections[channel_id][user_id] = websocket
    
    def disconnect(self, channel_id: int, user_id: int):
        """Disconnect a user from a channel"""
        if channel_id in self.active_connections:
            if user_id in self.active_connections[channel_id]:
                del self.active_connections[channel_id][user_id]
            
            # Clean up empty channels
            if not self.active_connections[channel_id]:
                del self.active_connections[channel_id]
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific websocket"""
        await websocket.send_text(message)
    
    async def broadcast_to_channel(self, message: dict, channel_id: int, exclude_user: int = None):
        """Broadcast a message to all users in a channel"""
        if channel_id not in self.active_connections:
            return
        
        message_json = json.dumps(message)
        
        # Send to all connections in the channel
        disconnected_users = []
        for user_id, connection in self.active_connections[channel_id].items():
            if exclude_user and user_id == exclude_user:
                continue
            
            try:
                await connection.send_text(message_json)
            except Exception as e:
                print(f"Error sending to user {user_id}: {e}")
                disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            self.disconnect(channel_id, user_id)
    
    def get_channel_users(self, channel_id: int) -> List[int]:
        """Get list of user IDs in a channel"""
        if channel_id not in self.active_connections:
            return []
        return list(self.active_connections[channel_id].keys())
    
    def is_user_online(self, user_id: int, channel_id: int) -> bool:
        """Check if a user is online in a specific channel"""
        if channel_id not in self.active_connections:
            return False
        return user_id in self.active_connections[channel_id]

manager = ConnectionManager()
