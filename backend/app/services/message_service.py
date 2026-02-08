from sqlalchemy.orm import Session
from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate
from typing import List
from fastapi import HTTPException, status

class MessageService:
    @staticmethod
    def create_message(db: Session, message: MessageCreate, user_id: int) -> Message:
        db_message = Message(
            content=message.content,
            user_id=user_id,
            channel_id=message.channel_id
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    
    @staticmethod
    def get_channel_messages(
        db: Session, 
        channel_id: int, 
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """Get messages for a channel with pagination"""
        messages = db.query(Message).filter(
            Message.channel_id == channel_id
        ).order_by(
            Message.created_at.desc()
        ).limit(limit).offset(offset).all()
        
        # Reverse to get chronological order
        return list(reversed(messages))
