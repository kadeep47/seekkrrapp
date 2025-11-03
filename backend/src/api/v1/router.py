"""Main API v1 router."""

from fastapi import APIRouter
from src.common.config import get_settings

settings = get_settings()

# Create main API router
api_router = APIRouter(prefix=settings.api_v1_prefix)

# Import and include sub-routers
from src.auth.router import router as auth_router
# from src.users.router import router as users_router
# from src.quests.router import router as quests_router
# from src.rewards.router import router as rewards_router
# from src.social.router import router as social_router

# Include routers
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# api_router.include_router(users_router, prefix="/users", tags=["Users"])
# api_router.include_router(quests_router, prefix="/quests", tags=["Quests"])
# api_router.include_router(rewards_router, prefix="/rewards", tags=["Rewards"])
# api_router.include_router(social_router, prefix="/social", tags=["Social"])


@api_router.get("/")
async def api_root():
    """API v1 root endpoint."""
    return {
        "message": "Seeker API v1",
        "version": "1.0.0",
        "available_endpoints": {
            "auth": "/auth - Authentication endpoints (register, login, logout)",
            "users": "/users - User management (coming soon)", 
            "quests": "/quests - Quest management (coming soon)",
            "rewards": "/rewards - Reward system (coming soon)",
            "social": "/social - Social features (coming soon)"
        }
    }