-- Initialize Seeker database
-- This script runs when the PostgreSQL container starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- Create database if it doesn't exist (handled by Docker environment)
-- The database 'seeker_dev' is created automatically by the POSTGRES_DB environment variable

-- Set timezone
SET timezone = 'UTC';