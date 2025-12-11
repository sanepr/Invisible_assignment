"""Group schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GroupCreate(BaseModel):
    """Schema for creating a new group."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class GroupMember(BaseModel):
    """Schema for group member information."""
    user_id: int
    username: str
    joined_at: datetime
    
    class Config:
        from_attributes = True


class GroupResponse(BaseModel):
    """Schema for group response."""
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    members: Optional[List[GroupMember]] = None
    
    class Config:
        from_attributes = True


class AddUserToGroup(BaseModel):
    """Schema for adding a user to a group."""
    user_id: int
