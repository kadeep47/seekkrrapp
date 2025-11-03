#!/usr/bin/env python3
"""Database initialization script."""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from database.config import engine, Base, test_db_connection, test_redis_connection
from database.seeds import seed_database
from common.logging import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


def init_database(seed_data: bool = True):
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
        
        # Seed database with development data
        if seed_data:
            logger.info("Seeding database with development data...")
            seed_result = seed_database()
            logger.info(f"Database seeded successfully: {seed_result}")
        
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize the database")
    parser.add_argument("--no-seed", action="store_true", help="Skip seeding development data")
    args = parser.parse_args()
    
    success = init_database(seed_data=not args.no_seed)
    sys.exit(0 if success else 1)