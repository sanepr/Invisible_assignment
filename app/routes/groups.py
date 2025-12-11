"""Group management routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.group import GroupCreate, GroupResponse, GroupDetailResponse, AddUserToGroup, GroupMember
from app.models.group import Group, UserGroup
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    group_data: GroupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new group and add creator as first member."""
    new_group = Group(
        name=group_data.name,
        description=group_data.description
    )
    
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    
    # Add creator to the group
    user_group = UserGroup(user_id=current_user.id, group_id=new_group.id)
    db.add(user_group)
    db.commit()
    
    return new_group


@router.get("", response_model=List[GroupResponse])
async def list_user_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all groups the current user is a member of."""
    user_groups = db.query(Group).join(UserGroup).filter(
        UserGroup.user_id == current_user.id
    ).all()
    
    return user_groups


@router.get("/{group_id}", response_model=GroupDetailResponse)
async def get_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of a specific group."""
    # Check if group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check if user is a member of the group
    is_member = db.query(UserGroup).filter(
        UserGroup.group_id == group_id,
        UserGroup.user_id == current_user.id
    ).first()
    
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this group"
        )
    
    # Get group members
    members_data = db.query(UserGroup, User).join(User).filter(
        UserGroup.group_id == group_id
    ).all()
    
    members = [
        GroupMember(
            user_id=user.id,
            username=user.username,
            joined_at=user_group.joined_at
        )
        for user_group, user in members_data
    ]
    
    # Create response with members
    group_response = GroupDetailResponse(
        id=group.id,
        name=group.name,
        description=group.description,
        created_at=group.created_at,
        members=members
    )
    
    return group_response


@router.post("/{group_id}/members", status_code=status.HTTP_201_CREATED)
async def add_user_to_group(
    group_id: int,
    member_data: AddUserToGroup,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a user to a group."""
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
    
    # Check if user to add exists
    user_to_add = db.query(User).filter(User.id == member_data.user_id).first()
    if not user_to_add:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is already a member
    existing_membership = db.query(UserGroup).filter(
        UserGroup.group_id == group_id,
        UserGroup.user_id == member_data.user_id
    ).first()
    
    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this group"
        )
    
    # Add user to group
    new_membership = UserGroup(user_id=member_data.user_id, group_id=group_id)
    db.add(new_membership)
    db.commit()
    
    return {"message": "User added to group successfully"}
