"""Common response models and utilities."""

from typing import Any, Dict, Optional, Generic, TypeVar
from pydantic import BaseModel
from datetime import datetime

T = TypeVar('T')


class PaginationInfo(BaseModel):
    """Pagination information model."""
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    timestamp: datetime = datetime.utcnow()
    request_id: Optional[str] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated API response."""
    success: bool = True
    data: list[T]
    pagination: PaginationInfo
    timestamp: datetime = datetime.utcnow()
    request_id: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: Dict[str, Any]
    timestamp: datetime = datetime.utcnow()
    request_id: Optional[str] = None


def create_response(
    data: Any = None,
    message: str = None,
    request_id: str = None
) -> ApiResponse:
    """Create a standard API response."""
    return ApiResponse(
        data=data,
        message=message,
        request_id=request_id
    )


def create_paginated_response(
    data: list,
    page: int,
    page_size: int,
    total_items: int,
    request_id: str = None
) -> PaginatedResponse:
    """Create a paginated API response."""
    total_pages = (total_items + page_size - 1) // page_size
    
    pagination = PaginationInfo(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )
    
    return PaginatedResponse(
        data=data,
        pagination=pagination,
        request_id=request_id
    )


def create_error_response(
    code: str,
    message: str,
    details: Dict[str, Any] = None,
    request_id: str = None
) -> ErrorResponse:
    """Create an error response."""
    return ErrorResponse(
        error={
            "code": code,
            "message": message,
            "details": details or {}
        },
        request_id=request_id
    )