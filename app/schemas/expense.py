"""Expense schemas."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List
from datetime import datetime


class ExpenseCreate(BaseModel):
    """Schema for creating a new expense."""
    group_id: int
    amount: float = Field(..., gt=0)
    description: Optional[str] = None


class ExpenseResponse(BaseModel):
    """Schema for expense response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    group_id: int
    paid_by_user_id: int
    amount: float
    description: Optional[str] = None
    created_at: datetime


class BalanceSummary(BaseModel):
    """Schema for balance summary response."""
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    username: str
    balance: float  # Positive means owed to user, negative means user owes


class GroupBalanceResponse(BaseModel):
    """Schema for group balance summary."""
    group_id: int
    group_name: str
    balances: List[BalanceSummary]
