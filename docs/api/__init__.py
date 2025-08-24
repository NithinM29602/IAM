"""
API Documentation

Contains OpenAPI specifications and API documentation files.
"""

import json
import os

def load_openapi_spec():
    """Load OpenAPI specification from JSON file"""
    current_dir = os.path.dirname(__file__)
    spec_path = os.path.join(current_dir, "openapi.json")
    
    if os.path.exists(spec_path):
        with open(spec_path, 'r') as f:
            return json.load(f)
    return None

__all__ = ["load_openapi_spec"]
