"""Tests for authentication system."""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from src.database.models import Base, User, UserStats
from src.database.config import get_db
from src.auth.security import (
    get_password_hash, verify_password, create_access_token, 
    create_refresh_token, verify_token, authenticate_user
)

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def db_session():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("testpassword123"),
        first_name="Test",
        last_name="User",
        display_name="Test User",
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    
    # Create user stats
    user_stats = UserStats(
        user_id=user.id,
        quests_completed=0,
        quests_joined=0,
        total_points=0
    )
    db_session.add(user_stats)
    
    db_session.commit()
    db_session.refresh(user)
    return user


class TestPasswordHashing:
    """Test password hashing functions."""
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False
    
    def test_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes."""
        password1 = "password123"
        password2 = "password456"
        
        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)
        
        assert hash1 != hash2


class TestJWTTokens:
    """Test JWT token creation and verification."""
    
    def test_create_access_token(self):
        """Test access token creation."""
        data = {"sub": "user123", "email": "test@example.com"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_refresh_token(self):
        """Test refresh token creation."""
        data = {"sub": "user123", "email": "test@example.com"}
        token = create_refresh_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_valid_token(self):
        """Test verification of valid token."""
        data = {"sub": "user123", "email": "test@example.com"}
        token = create_access_token(data)
        
        payload = verify_token(token, "access")
        
        assert payload["sub"] == "user123"
        assert payload["email"] == "test@example.com"
        assert payload["type"] == "access"
    
    def test_verify_expired_token(self):
        """Test verification of expired token."""
        data = {"sub": "user123", "email": "test@example.com"}
        # Create token that expires immediately
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        
        with pytest.raises(Exception):  # Should raise HTTPException
            verify_token(token, "access")
    
    def test_verify_wrong_token_type(self):
        """Test verification with wrong token type."""
        data = {"sub": "user123", "email": "test@example.com"}
        token = create_access_token(data)
        
        with pytest.raises(Exception):  # Should raise HTTPException
            verify_token(token, "refresh")


class TestAuthentication:
    """Test authentication functions."""
    
    def test_authenticate_valid_user(self, db_session, test_user):
        """Test authentication with valid credentials."""
        user = authenticate_user(db_session, "test@example.com", "testpassword123")
        
        assert user is not None
        assert user.email == "test@example.com"
        assert user.id == test_user.id
    
    def test_authenticate_invalid_email(self, db_session):
        """Test authentication with invalid email."""
        user = authenticate_user(db_session, "nonexistent@example.com", "password")
        
        assert user is None
    
    def test_authenticate_invalid_password(self, db_session, test_user):
        """Test authentication with invalid password."""
        user = authenticate_user(db_session, "test@example.com", "wrongpassword")
        
        assert user is None
    
    def test_authenticate_inactive_user(self, db_session, test_user):
        """Test authentication with inactive user."""
        test_user.is_active = False
        db_session.commit()
        
        user = authenticate_user(db_session, "test@example.com", "testpassword123")
        
        assert user is None


class TestAuthEndpoints:
    """Test authentication API endpoints."""
    
    def test_register_new_user(self):
        """Test user registration."""
        user_data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "username": "newuser",
            "first_name": "New",
            "last_name": "User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["user"]["email"] == "newuser@example.com"
        assert data["data"]["user"]["username"] == "newuser"
        assert "tokens" in data["data"]
        assert "access_token" in data["data"]["tokens"]
        assert "refresh_token" in data["data"]["tokens"]
    
    def test_register_duplicate_email(self, test_user):
        """Test registration with duplicate email."""
        user_data = {
            "email": "test@example.com",  # Same as test_user
            "password": "password123",
            "username": "differentuser"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_weak_password(self):
        """Test registration with weak password."""
        user_data = {
            "email": "weakpass@example.com",
            "password": "123",  # Too short
            "username": "weakuser"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 400
        assert "Password must be at least 8 characters" in response.json()["detail"]
    
    def test_login_valid_credentials(self, test_user):
        """Test login with valid credentials."""
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["user"]["email"] == "test@example.com"
        assert "tokens" in data["data"]
        assert "access_token" in data["data"]["tokens"]
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]
    
    def test_get_current_user_info(self, test_user):
        """Test getting current user information."""
        # First login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        login_response = client.post("/api/v1/auth/login", json=login_data)
        token = login_response.json()["data"]["tokens"]["access_token"]
        
        # Get user info with token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == "test@example.com"
        assert data["data"]["username"] == "testuser"
    
    def test_get_current_user_info_no_token(self):
        """Test getting user info without token."""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 401
        assert "Authentication required" in response.json()["detail"]
    
    def test_get_current_user_info_invalid_token(self):
        """Test getting user info with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]
    
    def test_refresh_token(self, test_user):
        """Test token refresh."""
        # First login to get tokens
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        login_response = client.post("/api/v1/auth/login", json=login_data)
        refresh_token = login_response.json()["data"]["tokens"]["refresh_token"]
        
        # Refresh token
        response = client.post(f"/api/v1/auth/refresh?refresh_token={refresh_token}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"
    
    def test_refresh_token_invalid(self):
        """Test refresh with invalid token."""
        response = client.post("/api/v1/auth/refresh?refresh_token=invalid_token")
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]
    
    def test_logout(self, test_user):
        """Test user logout."""
        # First login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        login_response = client.post("/api/v1/auth/login", json=login_data)
        token = login_response.json()["data"]["tokens"]["access_token"]
        
        # Logout
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/api/v1/auth/logout", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "Logged out successfully" in data["data"]["message"]
    
    def test_validate_token(self, test_user):
        """Test token validation."""
        # First login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        login_response = client.post("/api/v1/auth/login", json=login_data)
        token = login_response.json()["data"]["tokens"]["access_token"]
        
        # Validate token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/validate-token", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["valid"] is True
        assert data["data"]["email"] == "test@example.com"