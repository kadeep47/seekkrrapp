"""Authentication service layer."""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.database.models import User, UserStats
from src.database.schemas import UserCreate, RegisterRequest
from src.auth.security import get_password_hash, authenticate_user, create_tokens_for_user
from src.common.exceptions import ConflictError, AuthenticationError, ValidationError


class AuthService:
    """Authentication service class."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def register_user(self, user_data: RegisterRequest) -> Dict[str, Any]:
        """Register a new user."""
        # Check if user already exists
        existing_user = self.db.query(User).filter(
            (User.email == user_data.email) | 
            (User.username == user_data.username if user_data.username else False)
        ).first()
        
        if existing_user:
            if existing_user.email == user_data.email:
                raise ConflictError("Email already registered")
            else:
                raise ConflictError("Username already taken")
        
        # Validate password strength
        if len(user_data.password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        # Create new user
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=get_password_hash(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            display_name=user_data.first_name or user_data.username,
            is_active=True,
            is_verified=False  # Email verification required
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        # Create user stats
        user_stats = UserStats(
            user_id=user.id,
            quests_completed=0,
            quests_joined=0,
            quests_created=0,
            total_points=0,
            current_streak=0,
            longest_streak=0,
            friends_count=0,
            groups_joined=0,
            groups_created=0,
            total_distance_traveled=0.0
        )
        
        self.db.add(user_stats)
        self.db.commit()
        
        # Create tokens
        tokens = create_tokens_for_user(user)
        
        return {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "display_name": user.display_name,
                "is_verified": user.is_verified,
                "created_at": user.created_at.isoformat()
            },
            "tokens": tokens
        }
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login a user with email and password."""
        user = authenticate_user(self.db, email, password)
        
        if not user:
            raise AuthenticationError("Invalid email or password")
        
        # Update last login time
        user.last_login_at = datetime.utcnow()
        self.db.commit()
        
        # Create tokens
        tokens = create_tokens_for_user(user)
        
        return {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "display_name": user.display_name,
                "is_verified": user.is_verified,
                "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None
            },
            "tokens": tokens
        }
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            user_uuid = uuid.UUID(user_id)
            return self.db.query(User).filter(User.id == user_uuid).first()
        except ValueError:
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def verify_email(self, user_id: str) -> bool:
        """Verify user email."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_verified = True
        user.email_verified_at = datetime.utcnow()
        self.db.commit()
        return True
    
    def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """Change user password."""
        user = self.get_user_by_id(user_id)
        if not user:
            raise AuthenticationError("User not found")
        
        # Verify current password
        if not authenticate_user(self.db, user.email, current_password):
            raise AuthenticationError("Current password is incorrect")
        
        # Validate new password
        if len(new_password) < 8:
            raise ValidationError("New password must be at least 8 characters long")
        
        # Update password
        user.password_hash = get_password_hash(new_password)
        self.db.commit()
        return True
    
    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate user account."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        self.db.commit()
        return True
    
    def reactivate_user(self, user_id: str) -> bool:
        """Reactivate user account."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = True
        self.db.commit()
        return True