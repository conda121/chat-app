from sqlalchemy.orm import Session
from app.models.channel import Channel
from app.models.user import User
from app.schemas.channel import ChannelCreate
from fastapi import HTTPException, status
from typing import List

class ChannelService:
    @staticmethod
    def create_channel(db: Session, channel: ChannelCreate, user_id: int) -> Channel:
        # Check if channel name exists
        db_channel = db.query(Channel).filter(Channel.name == channel.name).first()
        if db_channel:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Channel name already exists"
            )
        
        # Create channel
        db_channel = Channel(
            name=channel.name,
            description=channel.description,
            created_by=user_id
        )
        
        # Add creator as member
        creator = db.query(User).filter(User.id == user_id).first()
        db_channel.members.append(creator)
        
        db.add(db_channel)
        db.commit()
        db.refresh(db_channel)
        return db_channel
    
    @staticmethod
    def get_channels(db: Session, user_id: int) -> List[Channel]:
        """Get all channels where user is a member"""
        user = db.query(User).filter(User.id == user_id).first()
        return user.channels
    
    @staticmethod
    def get_channel(db: Session, channel_id: int) -> Channel:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found"
            )
        return channel
    
    @staticmethod
    def join_channel(db: Session, channel_id: int, user_id: int):
        """Add user to channel"""
        channel = ChannelService.get_channel(db, channel_id)
        user = db.query(User).filter(User.id == user_id).first()
        
        if user not in channel.members:
            channel.members.append(user)
            db.commit()
        
        return channel
    
    @staticmethod
    def leave_channel(db: Session, channel_id: int, user_id: int):
        """Remove user from channel"""
        channel = ChannelService.get_channel(db, channel_id)
        user = db.query(User).filter(User.id == user_id).first()
        
        if user in channel.members:
            channel.members.remove(user)
            db.commit()
        
        return {"message": "Left channel successfully"}
