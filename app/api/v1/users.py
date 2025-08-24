from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.schemas import (
    UserCreate, UserUpdate, UserResponse, UserListResponse, 
    MessageResponse, UserStatus
)
from app.models.user import User
from app.services.user_service import UserService
from app.dependencies.db import get_user_service
from app.core.security import verify_token

router = APIRouter()
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """Get current authenticated user"""
    user_id = verify_token(credentials.credentials)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

async def require_admin(current_user: User = Depends(get_current_user)):
    """Require admin role"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_admin)
):
    """Create a new user (Admin only)"""
    return await user_service.create_user(user_data)

@router.get("/users/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile"""
    return current_user

@router.put("/users/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Update current user's profile"""
    # Users can only update their own non-role/status fields
    if user_update.role is not None or user_update.status is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update role or status"
        )
    
    return await user_service.update_user(str(current_user.id), user_update)

@router.get("/users", response_model=UserListResponse)
async def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service)
):
    """Get list of users (Admin only)"""
    skip = (page - 1) * size
    users = await user_service.get_users(skip=skip, limit=size)
    total = await user_service.get_users_count()
    
    return UserListResponse(
        users=users,
        total=total,
        page=page,
        size=size
    )

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    current_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service)
):
    """Get user by ID (Admin only)"""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service)
):
    """Update user (Admin only)"""
    return await user_service.update_user(user_id, user_update)

@router.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service)
):
    """Delete user (Admin only)"""
    if user_id == str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    await user_service.delete_user(user_id)
    return MessageResponse(message="User deleted successfully")

@router.patch("/users/{user_id}/status", response_model=UserResponse)
async def change_user_status(
    user_id: str,
    status: UserStatus,
    current_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service)
):
    """Change user status (Admin only)"""
    if user_id == str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own status"
        )
    
    return await user_service.change_user_status(user_id, status)
