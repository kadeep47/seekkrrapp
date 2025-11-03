"""Tests for the main FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Welcome to Seeker API" in data["data"]["message"]
    assert data["data"]["version"] == "1.0.0"


@patch("src.database.config.test_db_connection", return_value=True)
@patch("src.database.config.test_redis_connection", return_value=True)
def test_health_endpoint_healthy(mock_redis, mock_db):
    """Test health endpoint when services are healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"
    assert data["data"]["checks"]["database"] == "connected"
    assert data["data"]["checks"]["redis"] == "connected"


@patch("src.database.config.test_db_connection", return_value=False)
@patch("src.database.config.test_redis_connection", return_value=False)
def test_health_endpoint_unhealthy(mock_redis, mock_db):
    """Test health endpoint when services are unhealthy."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "unhealthy"
    assert data["data"]["checks"]["database"] == "disconnected"
    assert data["data"]["checks"]["redis"] == "disconnected"


def test_api_status_endpoint():
    """Test the API status endpoint."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["api_version"] == "v1"
    assert data["data"]["status"] == "operational"
    assert "features" in data["data"]


def test_api_v1_root():
    """Test the API v1 root endpoint."""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Seeker API v1"
    assert "available_endpoints" in data


def test_cors_headers():
    """Test CORS headers are present."""
    response = client.get("/")
    assert "access-control-allow-origin" in response.headers
    

def test_request_id_header():
    """Test that request ID is added to response headers."""
    response = client.get("/")
    assert "x-request-id" in response.headers
    assert "x-process-time" in response.headers


def test_404_error_handling():
    """Test 404 error handling."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert "error" in data