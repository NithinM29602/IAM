"""
Dependencies module for IAM Service

Contains dependency injection functions for FastAPI endpoints.
Provides database services and authentication dependencies.
"""

from .db import get_auth_service, get_user_service

__all__ = [
    "get_auth_service",
    "get_user_service"
]
