#!/usr/bin/env python3
"""Database initialization script."""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from database.config import engine, Base, test_db_connection, test_redis_connection
from common.logging import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


def init_database():
    """Initialize the database."""
    logger.info("Initializing database...")
    
    try:
        # Test connections
        if not test_db_connection():
            logger.error("Database connection failed")
            return False
        
        if not test_redis_connection():
            logger.error("Redis connection failed")
            return False
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)