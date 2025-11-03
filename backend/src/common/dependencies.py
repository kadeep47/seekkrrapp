"""Common dependencies for FastAPI endpoints."""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import redis

from src.database.config import get_db, get_redis
from src.common.config import get_settings

settings = get_settings()
security = HTTPBearer(auto_error=False)


def get_current_request_id(request: Request) -> Optional[str]:
    """Get the current request ID from request state."""
    return getattr(request.state, "request_id", None)


def get_database_session() -> Session:
    """Get database session dependency."""
    return Depends(get_db)


def get_redis_client() -> redis.Redis:
    """Get Redis client dependency."""
    return Depends(get_redis)


def get_pagination_params(
    page: int = 1,
    page_size: int = 20,
    max_page_size: int = 100
) -> dict:
    """Get pagination parameters with validation."""
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page number must be greater than 0"
        )
    
    if page_size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be greater than 0"
        )
    
    if page_size > max_page_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Page size cannot exceed {max_page_size}"
        )
    
    return {
        "page": page,
        "page_size": page_size,
        "offset": (page - 1) * page_size
    }


# Authentication dependencies are now in src.auth.dependencies
# Import them here for backward compatibility
from src.auth.dependencies import get_current_user_optional as get_optional_current_user
from src.auth.dependencies import get_current_user