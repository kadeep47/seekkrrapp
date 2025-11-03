"""OpenAPI customization and documentation."""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import Dict, Any


def custom_openapi(app: FastAPI) -> Dict[str, Any]:
    """Generate custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Seeker API",
        version="1.0.0",
        description="""
        ## Seeker Platform API
        
        A comprehensive location-based questing platform API that provides:
        
        ### Features
        - **Authentication**: JWT-based authentication with OAuth support
        - **User Management**: User profiles, preferences, and statistics
        - **Quest System**: Location-based quests with progress tracking
        - **Reward Engine**: Points, achievements, and leaderboards
        - **Social Features**: Groups, friends, and activity feeds
        
        ### API Design
        - RESTful API design with consistent response formats
        - Comprehensive error handling and validation
        - Rate limiting and security controls
        - OpenAPI 3.0 specification with auto-generated client SDKs
        
        ### Authentication
        Most endpoints require authentication using Bearer tokens:
        ```
        Authorization: Bearer <your-jwt-token>
        ```
        
        ### Response Format
        All API responses follow a consistent format:
        ```json
        {
            "success": true,
            "data": {...},
            "message": "Optional message",
            "timestamp": "2024-01-01T00:00:00Z",
            "request_id": "uuid"
        }
        ```
        
        ### Error Handling
        Errors are returned with appropriate HTTP status codes and detailed information:
        ```json
        {
            "success": false,
            "error": {
                "code": "ErrorType",
                "message": "Human readable message",
                "details": {...}
            },
            "request_id": "uuid",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        ```
        """,
        routes=app.routes,
    )
    
    # Add custom info
    openapi_schema["info"]["contact"] = {
        "name": "Seeker API Support",
        "email": "support@seeker.com"
    }
    
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
    
    # Add servers
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.seeker.com",
            "description": "Production server"
        }
    ]
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Add tags
    openapi_schema["tags"] = [
        {
            "name": "Authentication",
            "description": "User authentication and authorization"
        },
        {
            "name": "Users",
            "description": "User management and profiles"
        },
        {
            "name": "Quests",
            "description": "Location-based quest management"
        },
        {
            "name": "Rewards",
            "description": "Reward system and achievements"
        },
        {
            "name": "Social",
            "description": "Social features and group management"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def setup_openapi(app: FastAPI) -> None:
    """Set up custom OpenAPI schema for the app."""
    app.openapi = lambda: custom_openapi(app)