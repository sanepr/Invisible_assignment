"""Group schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class GroupCreate(BaseModel):
    """Schema for creating a new group."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class GroupMember(BaseModel):
    """Schema for group member information."""
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    username: str
    joined_at: datetime


class GroupResponse(BaseModel):
    """Schema for group response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime


class GroupDetailResponse(BaseModel):
    """Schema for detailed group response with members."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    members: List[GroupMember]


class AddUserToGroup(BaseModel):
    """Schema for adding a user to a group."""
    user_id: int
