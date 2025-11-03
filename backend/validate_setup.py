#!/usr/bin/env python3
"""Validate the backend setup."""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def validate_imports():
    """Validate that all imports work correctly."""
    try:
        print("Validating imports...")
        
        # Test basic imports
        from common.config import get_settings
        from common.middleware import RequestLoggingMiddleware
        from common.exceptions import SeekerException
        from common.responses import create_response
        from common.dependencies import get_pagination_params
        from common.logging import setup_logging
        from common.openapi import setup_openapi
        from database.config import Base, get_db
        from api.v1.router import api_router
        
        print("✓ All imports successful")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def validate_settings():
    """Validate settings configuration."""
    try:
        print("Validating settings...")
        
        from common.config import get_settings
        settings = get_settings()
        
        assert settings.app_name == "Seeker API"
        assert settings.app_version == "1.0.0"
        assert settings.api_v1_prefix == "/api/v1"
        
        print("✓ Settings validation successful")
        return True
        
    except Exception as e:
        print(f"✗ Settings validation error: {e}")
        return False


def validate_fastapi_app():
    """Validate FastAPI application creation."""
    try:
        print("Validating FastAPI application...")
        
        # Import main app
        sys.path.append(os.path.dirname(__file__))
        from main import app
        
        assert app.title == "Seeker API"
        assert app.version == "1.0.0"
        
        print("✓ FastAPI application validation successful")
        return True
        
    except Exception as e:
        print(f"✗ FastAPI application validation error: {e}")
        return False


def main():
    """Run all validations."""
    print("=== Backend Setup Validation ===\n")
    
    validations = [
        validate_imports,
        validate_settings,
        validate_fastapi_app
    ]
    
    results = []
    for validation in validations:
        results.append(validation())
        print()
    
    if all(results):
        print("🎉 All validations passed! Backend setup is complete.")
        return True
    else:
        print("❌ Some validations failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)