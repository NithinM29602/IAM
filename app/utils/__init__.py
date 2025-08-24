"""
Utils module for IAM Service

Contains utility functions and helpers including:
- Logging configuration
- Exception handling
- Common utilities
"""

from .logger import setup_logging
from .exception_handler import setup_exception_handlers

__all__ = [
    "setup_logging",
    "setup_exception_handlers"
]
