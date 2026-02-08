from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    channel_id: int

class Message(MessageBase):
    id: int
    user_id: int
    username: str  # We'll include username for convenience
    channel_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class WebSocketMessage(BaseModel):
    type: str  # "message", "user_joined", "user_left"
    content: str
    username: str
    channel_id: int
    timestamp: datetime
