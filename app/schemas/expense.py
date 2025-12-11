"""Expense schemas."""
from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class ExpenseCreate(BaseModel):
    """Schema for creating a new expense."""
    group_id: int
    amount: float = Field(..., gt=0)
    description: Optional[str] = None


class ExpenseResponse(BaseModel):
    """Schema for expense response."""
    id: int
    group_id: int
    paid_by_user_id: int
    amount: float
    description: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class BalanceSummary(BaseModel):
    """Schema for balance summary response."""
    user_id: int
    username: str
    balance: float  # Positive means owed to user, negative means user owes
    
    class Config:
        from_attributes = True


class GroupBalanceResponse(BaseModel):
    """Schema for group balance summary."""
    group_id: int
    group_name: str
    balances: list[BalanceSummary]
