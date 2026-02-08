from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.channel import Channel, ChannelCreate, ChannelWithMembers
from app.services.channel_service import ChannelService

router = APIRouter()

@router.post("/", response_model=Channel, status_code=status.HTTP_201_CREATED)
def create_channel(
    channel: ChannelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new channel"""
    return ChannelService.create_channel(db, channel, current_user.id)

@router.get("/", response_model=List[Channel])
def get_my_channels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all channels where current user is a member"""
    return ChannelService.get_channels(db, current_user.id)

@router.get("/{channel_id}", response_model=Channel)
def get_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific channel"""
    return ChannelService.get_channel(db, channel_id)

@router.post("/{channel_id}/join", response_model=Channel)
def join_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Join a channel"""
    return ChannelService.join_channel(db, channel_id, current_user.id)

@router.post("/{channel_id}/leave")
def leave_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Leave a channel"""
    return ChannelService.leave_channel(db, channel_id, current_user.id)
