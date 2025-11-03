"""Common exception classes and handlers."""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


class SeekerException(Exception):
    """Base exception class for Seeker application."""
    
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(SeekerException):
    """Authentication related errors."""
    
    def __init__(self, message: str = "Authentication failed", details: dict = None):
        super().__init__(message, 401, details)


class AuthorizationError(SeekerException):
    """Authorization related errors."""
    
    def __init__(self, message: str = "Access denied", details: dict = None):
        super().__init__(message, 403, details)


class NotFoundError(SeekerException):
    """Resource not found errors."""
    
    def __init__(self, message: str = "Resource not found", details: dict = None):
        super().__init__(message, 404, details)


class ValidationError(SeekerException):
    """Validation related errors."""
    
    def __init__(self, message: str = "Validation failed", details: dict = None):
        super().__init__(message, 422, details)


class ConflictError(SeekerException):
    """Resource conflict errors."""
    
    def __init__(self, message: str = "Resource conflict", details: dict = None):
        super().__init__(message, 409, details)


async def seeker_exception_handler(request: Request, exc: SeekerException):
    """Handle custom Seeker exceptions."""
    logger.error(f"SeekerException: {exc.message} - Details: {exc.details}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details
            },
            "request_id": getattr(request.state, "request_id", None),
            "timestamp": "2024-01-01T00:00:00Z"  # Will be replaced with actual timestamp
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    logger.error(f"HTTPException: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTPException",
                "message": exc.detail,
                "details": {}
            },
            "request_id": getattr(request.state, "request_id", None),
            "timestamp": "2024-01-01T00:00:00Z"
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions."""
    logger.error(f"ValidationError: {exc.errors()}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "ValidationError",
                "message": "Request validation failed",
                "details": {
                    "validation_errors": exc.errors()
                }
            },
            "request_id": getattr(request.state, "request_id", None),
            "timestamp": "2024-01-01T00:00:00Z"
        }
    )