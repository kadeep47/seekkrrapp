"""Database configuration and connection management."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import redis
from typing import Generator

# Import models to ensure they are registered with Base
from .models import Base

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://seeker:dev_password@localhost:5432/seeker_dev")

# Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=os.getenv("DEBUG", "false").lower() == "true"
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Redis connection
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


def get_db() -> Generator:
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    """Dependency to get Redis client."""
    return redis_client


# Test database connection
def test_db_connection():
    """Test database connection."""
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


# Test Redis connection
def test_redis_connection():
    """Test Redis connection."""
    try:
        redis_client.ping()
        return True
    except Exception as e:
        print(f"Redis connection failed: {e}")
        return False