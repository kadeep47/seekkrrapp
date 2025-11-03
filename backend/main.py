"""Main FastAPI application."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Import application components
from src.common.config import get_settings
from src.common.middleware import RequestLoggingMiddleware
from src.common.exceptions import (
    SeekerException,
    seeker_exception_handler,
    http_exception_handler,
    validation_exception_handler
)
from src.common.responses import create_response
from src.database.config import test_db_connection, test_redis_connection
from src.api.v1.router import api_router
from src.common.openapi import setup_openapi

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Location-based questing platform API with comprehensive features",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.debug
)

# Add middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(SeekerException, seeker_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include API router
app.include_router(api_router)

# Setup custom OpenAPI
setup_openapi(app)


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Test database connection
    if test_db_connection():
        logger.info("Database connection successful")
    else:
        logger.error("Database connection failed")
    
    # Test Redis connection
    if test_redis_connection():
        logger.info("Redis connection successful")
    else:
        logger.error("Redis connection failed")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info(f"Shutting down {settings.app_name}")


@app.get("/")
async def root(request: Request):
    """Root endpoint with API information."""
    return create_response(
        data={
            "message": f"Welcome to {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs",
            "redoc": "/redoc",
            "api_prefix": settings.api_v1_prefix,
            "timestamp": datetime.utcnow().isoformat()
        },
        message="API is running successfully",
        request_id=getattr(request.state, "request_id", None)
    )


@app.get("/health")
async def health_check(request: Request):
    """Comprehensive health check endpoint."""
    db_status = test_db_connection()
    redis_status = test_redis_connection()
    
    overall_status = "healthy" if db_status and redis_status else "unhealthy"
    
    return create_response(
        data={
            "status": overall_status,
            "service": "seeker-api",
            "version": settings.app_version,
            "checks": {
                "database": "connected" if db_status else "disconnected",
                "redis": "connected" if redis_status else "disconnected"
            },
            "timestamp": datetime.utcnow().isoformat()
        },
        request_id=getattr(request.state, "request_id", None)
    )


@app.get(f"{settings.api_v1_prefix}/status")
async def api_status(request: Request):
    """API status and feature availability."""
    return create_response(
        data={
            "api_version": "v1",
            "status": "operational",
            "features": {
                "authentication": "pending",
                "user_management": "pending",
                "quest_system": "pending",
                "reward_engine": "pending",
                "social_features": "pending"
            },
            "endpoints": {
                "docs": "/docs",
                "redoc": "/redoc",
                "health": "/health",
                "openapi": "/openapi.json"
            }
        },
        message="API v1 is operational",
        request_id=getattr(request.state, "request_id", None)
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level=settings.log_level.lower(),
        reload=settings.debug
    )