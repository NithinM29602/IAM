"""
API v1 module

Version 1 of the IAM Service API endpoints.
Includes authentication and user management endpoints.
"""

from fastapi import APIRouter
from . import auth, users

# Create v1 router
router = APIRouter()

# Include all v1 endpoints
router.include_router(auth.router, tags=["Authentication"])
router.include_router(users.router, tags=["User Management"])

__all__ = ["router", "auth", "users"]
