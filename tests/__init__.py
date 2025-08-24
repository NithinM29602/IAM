"""
Tests module for IAM Service

Contains comprehensive test suite for all IAM Service functionality.
Includes unit tests, integration tests, and API endpoint tests.
"""

import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

# Test configuration
TEST_DATABASE_URL = "mongodb://localhost:27017"
TEST_DATABASE_NAME = "iam_service_test"

__all__ = [
    "pytest",
    "TestClient", 
    "AsyncIOMotorClient",
    "TEST_DATABASE_URL",
    "TEST_DATABASE_NAME"
]
