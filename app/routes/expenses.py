"""Expense management routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseResponse, GroupBalanceResponse, BalanceSummary
from app.models.expense import Expense
from app.models.group import Group, UserGroup
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def add_expense(
    expense_data: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new expense to a group."""
    # Check if group exists
    group = db.query(Group).filter(Group.id == expense_data.group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check if current user is a member of the group
    is_member = db.query(UserGroup).filter(
        UserGroup.group_id == expense_data.group_id,
        UserGroup.user_id == current_user.id
    ).first()
    
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this group"
        )
    
    # Create new expense
    new_expense = Expense(
        group_id=expense_data.group_id,
        paid_by_user_id=current_user.id,
        amount=expense_data.amount,
        description=expense_data.description
    )
    
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    return new_expense


@router.get("/group/{group_id}", response_model=List[ExpenseResponse])
async def get_group_expenses(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all expenses for a specific group."""
    # Check if group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check if current user is a member of the group
    is_member = db.query(UserGroup).filter(
        UserGroup.group_id == group_id,
        UserGroup.user_id == current_user.id
    ).first()
    
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this group"
        )
    
    # Get all expenses for the group
    expenses = db.query(Expense).filter(Expense.group_id == group_id).order_by(
        Expense.created_at.desc()
    ).all()
    
    return expenses


@router.get("/group/{group_id}/balances", response_model=GroupBalanceResponse)
async def get_group_balances(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get balance summary for a group (assuming equal split)."""
    # Check if group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check if current user is a member of the group
    is_member = db.query(UserGroup).filter(
        UserGroup.group_id == group_id,
        UserGroup.user_id == current_user.id
    ).first()
    
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this group"
        )
    
    # Get all members of the group
    members = db.query(User).join(UserGroup).filter(
        UserGroup.group_id == group_id
    ).all()
    
    if not members:
        return GroupBalanceResponse(
            group_id=group_id,
            group_name=group.name,
            balances=[]
        )
    
    member_count = len(members)
    
    # Get all expenses for the group
    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
    
    # Calculate balances
    balances = {}
    for member in members:
        balances[member.id] = {
            "user_id": member.id,
            "username": member.username,
            "paid": 0.0,
            "share": 0.0
        }
    
    # Calculate total paid by each user and their share
    for expense in expenses:
        if expense.paid_by_user_id in balances:
            balances[expense.paid_by_user_id]["paid"] += expense.amount
        
        # Equal split among all members
        share_per_person = expense.amount / member_count
        for user_id in balances:
            balances[user_id]["share"] += share_per_person
    
    # Calculate net balance (positive = owed to user, negative = user owes)
    balance_summary = []
    for user_id, data in balances.items():
        net_balance = data["paid"] - data["share"]
        balance_summary.append(
            BalanceSummary(
                user_id=data["user_id"],
                username=data["username"],
                balance=round(net_balance, 2)
            )
        )
    
    return GroupBalanceResponse(
        group_id=group_id,
        group_name=group.name,
        balances=balance_summary
    )
