"""
API module for IAM Service

Contains all API endpoints and routing logic.
Organized by API versions for backward compatibility.
"""

from fastapi import APIRouter

# Main API router that includes all versions
api_router = APIRouter()

# Import and include version-specific routers
from .v1 import router as v1_router
api_router.include_router(v1_router, prefix="/v1")
