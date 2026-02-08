from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.message import Message
from app.services.message_service import MessageService

router = APIRouter()

@router.get("/channels/{channel_id}/messages", response_model=List[Message])
def get_channel_messages(
    channel_id: int,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get messages for a specific channel"""
    messages = MessageService.get_channel_messages(db, channel_id, limit, offset)
    
    # Add username to each message
    result = []
    for msg in messages:
        message_dict = {
            "id": msg.id,
            "content": msg.content,
            "user_id": msg.user_id,
            "username": msg.user.username,
            "channel_id": msg.channel_id,
            "created_at": msg.created_at
        }
        result.append(message_dict)
    
    return result
