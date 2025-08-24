"""
Core module for IAM Service

Contains core functionality including:
- Configuration management
- Security utilities (JWT, password hashing)
- Rate limiting middleware
- Application settings
"""

from .config import settings
from .security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    verify_token
)

__all__ = [
    "settings",
    "create_access_token", 
    "create_refresh_token",
    "verify_password",
    "get_password_hash",
    "verify_token"
]
