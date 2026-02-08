from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ChannelBase(BaseModel):
    name: str
    description: Optional[str] = None

class ChannelCreate(ChannelBase):
    pass

class Channel(ChannelBase):
    id: int
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChannelWithMembers(Channel):
    member_count: int
