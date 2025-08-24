"""
Database module for IAM Service

Contains database connection management, schemas, and database utilities.
Uses MongoDB with Motor for async operations.
"""

from .database import get_database, connect_to_mongo, close_mongo_connection, get_db
from .schemas import (
    UserRole,
    UserStatus,
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenData,
    RefreshTokenRequest,
    MessageResponse,
    UserListResponse
)

__all__ = [
    # Database functions
    "get_database",
    "connect_to_mongo", 
    "close_mongo_connection",
    "get_db",
    # Schemas
    "UserRole",
    "UserStatus", 
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    "RefreshTokenRequest",
    "MessageResponse",
    "UserListResponse"
]
