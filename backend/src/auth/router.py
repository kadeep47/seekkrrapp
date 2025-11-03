"""Authentication router with all auth endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.database.schemas import (
    LoginRequest, RegisterRequest, Token, User as UserSchema
)
from src.database.models import User
from src.auth.service import AuthService
from src.auth.dependencies import get_auth_service, get_current_user, get_current_verified_user
from src.auth.security import refresh_access_token, verify_token, create_access_token
from src.auth.email import email_service
from src.common.responses import create_response
from src.common.exceptions import AuthenticationError, ConflictError, ValidationError
from src.common.dependencies import get_current_request_id
from datetime import timedelta

router = APIRouter()


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user account."""
    try:
        result = auth_service.register_user(user_data)
        
        return create_response(
            data=result,
            message="User registered successfully",
            request_id=getattr(request.state, "request_id", None)
        )
        
    except (ConflictError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=dict)
async def login(
    login_data: LoginRequest,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Login with email and password."""
    try:
        result = auth_service.login_user(login_data.email, login_data.password)
        
        return create_response(
            data=result,
            message="Login successful",
            request_id=getattr(request.state, "request_id", None)
        )
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/refresh", response_model=dict)
async def refresh_token(
    refresh_token: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    try:
        result = refresh_access_token(refresh_token, db)
        
        return create_response(
            data=result,
            message="Token refreshed successfully",
            request_id=getattr(request.state, "request_id", None)
        )
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token"
        )


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Logout user (client should discard tokens)."""
    # In a more sophisticated implementation, you might:
    # 1. Add tokens to a blacklist
    # 2. Store active sessions in Redis
    # 3. Implement token revocation
    
    return create_response(
        data={"message": "Logged out successfully"},
        message="Please discard your tokens",
        request_id=getattr(request.state, "request_id", None)
    )


@router.get("/me", response_model=dict)
async def get_current_user_info(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Get current user information."""
    user_data = {
        "id": str(current_user.id),
        "email": current_user.email,
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "display_name": current_user.display_name,
        "bio": current_user.bio,
        "avatar_url": current_user.avatar_url,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "email_verified_at": current_user.email_verified_at.isoformat() if current_user.email_verified_at else None,
        "last_login_at": current_user.last_login_at.isoformat() if current_user.last_login_at else None,
        "profile_visibility": current_user.profile_visibility,
        "location_sharing": current_user.location_sharing,
        "preferred_city_id": str(current_user.preferred_city_id) if current_user.preferred_city_id else None,
        "created_at": current_user.created_at.isoformat(),
        "updated_at": current_user.updated_at.isoformat()
    }
    
    return create_response(
        data=user_data,
        message="User information retrieved successfully",
        request_id=getattr(request.state, "request_id", None)
    )


@router.post("/verify-email/{user_id}")
async def verify_email(
    user_id: str,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Verify user email address."""
    # In a real implementation, this would be called with a verification token
    # sent via email, not directly with user_id
    
    success = auth_service.verify_email(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return create_response(
        data={"verified": True},
        message="Email verified successfully",
        request_id=getattr(request.state, "request_id", None)
    )


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    request: Request,
    current_user: User = Depends(get_current_verified_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Change user password."""
    try:
        success = auth_service.change_password(
            str(current_user.id), 
            current_password, 
            new_password
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to change password"
            )
        
        return create_response(
            data={"changed": True},
            message="Password changed successfully",
            request_id=getattr(request.state, "request_id", None)
        )
        
    except (AuthenticationError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/deactivate")
async def deactivate_account(
    request: Request,
    current_user: User = Depends(get_current_verified_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Deactivate user account."""
    success = auth_service.deactivate_user(str(current_user.id))
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to deactivate account"
        )
    
    return create_response(
        data={"deactivated": True},
        message="Account deactivated successfully",
        request_id=getattr(request.state, "request_id", None)
    )


@router.post("/forgot-password")
async def forgot_password(
    email: str,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Send password reset email."""
    user = auth_service.get_user_by_email(email)
    
    if user:
        # Create password reset token (valid for 1 hour)
        reset_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "purpose": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        
        # In a real implementation, you'd use your frontend URL
        reset_link = f"https://seeker.com/reset-password?token={reset_token}"
        
        # Send email (this will fail silently if email is not configured)
        email_service.send_password_reset_email(user.email, reset_link)
    
    # Always return success to prevent email enumeration
    return create_response(
        data={"sent": True},
        message="If the email exists, a password reset link has been sent",
        request_id=getattr(request.state, "request_id", None)
    )


@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Reset password using reset token."""
    try:
        # Verify reset token
        payload = verify_token(token, "access")
        
        if payload.get("purpose") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )
        
        user = auth_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found"
            )
        
        # Validate new password
        if len(new_password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long"
            )
        
        # Update password
        from src.auth.security import get_password_hash
        user.password_hash = get_password_hash(new_password)
        auth_service.db.commit()
        
        return create_response(
            data={"reset": True},
            message="Password reset successfully",
            request_id=getattr(request.state, "request_id", None)
        )
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )


@router.get("/validate-token")
async def validate_token(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Validate if the current token is valid."""
    return create_response(
        data={
            "valid": True,
            "user_id": str(current_user.id),
            "email": current_user.email,
            "is_verified": current_user.is_verified
        },
        message="Token is valid",
        request_id=getattr(request.state, "request_id", None)
    )