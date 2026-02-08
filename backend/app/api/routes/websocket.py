from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.websocket.connection_manager import manager
from app.models.user import User
from app.services.message_service import MessageService
from app.schemas.message import MessageCreate
from jose import JWTError, jwt
from app.core.config import settings
from datetime import datetime
import json

router = APIRouter()

async def get_user_from_token(token: str, db: Session) -> User:
    """Get user from JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    
    user = db.query(User).filter(User.username == username).first()
    return user

@router.websocket("/ws/{channel_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    channel_id: int,
    token: str = Query(...),
):
    # Get database session
    db = next(get_db())
    
    try:
        # Authenticate user
        user = await get_user_from_token(token, db)
        if not user:
            await websocket.close(code=1008)  # Policy violation
            return
        
        # Connect to channel
        await manager.connect(websocket, channel_id, user.id)
        
        # Broadcast user joined
        join_message = {
            "type": "user_joined",
            "content": f"{user.username} joined the channel",
            "username": "System",
            "channel_id": channel_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        await manager.broadcast_to_channel(join_message, channel_id)
        
        # Listen for messages
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Save message to database
            message_create = MessageCreate(
                content=message_data["content"],
                channel_id=channel_id
            )
            db_message = MessageService.create_message(db, message_create, user.id)
            
            # Broadcast to all users in channel
            broadcast_message = {
                "type": "message",
                "id": db_message.id,
                "content": db_message.content,
                "username": user.username,
                "user_id": user.id,
                "channel_id": channel_id,
                "timestamp": db_message.created_at.isoformat()
            }
            await manager.broadcast_to_channel(broadcast_message, channel_id)
    
    except WebSocketDisconnect:
        # User disconnected
        manager.disconnect(channel_id, user.id)
        
        # Broadcast user left
        leave_message = {
            "type": "user_left",
            "content": f"{user.username} left the channel",
            "username": "System",
            "channel_id": channel_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        await manager.broadcast_to_channel(leave_message, channel_id)
    
    finally:
        db.close()
