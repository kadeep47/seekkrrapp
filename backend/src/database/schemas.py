"""Pydantic schemas for database models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum

# Enums
class QuestStatusEnum(str, Enum):
    DRAFT = "draft"
    UPCOMING = "upcoming"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class QuestDifficultyEnum(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class GroupRoleEnum(str, Enum):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    OWNER = "owner"


class FriendshipStatusEnum(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"


# Base schemas
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimestampSchema(BaseSchema):
    created_at: datetime
    updated_at: datetime


class UUIDSchema(BaseSchema):
    id: str


# City schemas
class CityBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    state_province: Optional[str] = Field(None, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timezone: Optional[str] = Field(None, max_length=50)
    population: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    is_active: bool = True
    metadata: Optional[Dict[str, Any]] = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    state_province: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    timezone: Optional[str] = Field(None, max_length=50)
    population: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class City(CityBase, UUIDSchema, TimestampSchema):
    pass


# Location schemas
class LocationBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius: float = Field(50.0, ge=1.0, le=1000.0)
    address: Optional[str] = Field(None, max_length=500)


class LocationCreate(LocationBase):
    city_id: str


class LocationUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    radius: Optional[float] = Field(None, ge=1.0, le=1000.0)
    address: Optional[str] = Field(None, max_length=500)


class Location(LocationBase, UUIDSchema, TimestampSchema):
    city_id: str
    city: Optional[City] = None


# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    display_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=500)
    profile_visibility: str = Field("public", regex="^(public|friends|private)$")
    location_sharing: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    preferred_city_id: Optional[str] = None


class UserUpdate(BaseSchema):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    display_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=500)
    preferred_city_id: Optional[str] = None
    profile_visibility: Optional[str] = Field(None, regex="^(public|friends|private)$")
    location_sharing: Optional[bool] = None


class User(UserBase, UUIDSchema, TimestampSchema):
    is_active: bool
    is_verified: bool
    email_verified_at: Optional[datetime]
    last_login_at: Optional[datetime]
    preferred_city_id: Optional[str]
    preferred_city: Optional[City] = None


class UserPublic(BaseSchema):
    """Public user information (for other users to see)."""
    id: str
    username: Optional[str]
    display_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime


# User Stats schemas
class UserStatsBase(BaseSchema):
    quests_completed: int = 0
    quests_joined: int = 0
    quests_created: int = 0
    total_points: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    friends_count: int = 0
    groups_joined: int = 0
    groups_created: int = 0
    total_distance_traveled: float = 0.0


class UserStats(UserStatsBase, UUIDSchema, TimestampSchema):
    user_id: str
    last_activity_at: Optional[datetime]


# Quest schemas
class QuestBase(BaseSchema):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    short_description: Optional[str] = Field(None, max_length=500)
    difficulty: QuestDifficultyEnum
    max_participants: int = Field(50, ge=1, le=1000)
    min_participants: int = Field(1, ge=1)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    estimated_duration: Optional[int] = Field(None, ge=1)  # minutes
    points_reward: int = Field(0, ge=0)
    quest_data: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = Field(None, max_length=500)


class QuestCreate(QuestBase):
    city_id: str


class QuestUpdate(BaseSchema):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    short_description: Optional[str] = Field(None, max_length=500)
    difficulty: Optional[QuestDifficultyEnum] = None
    status: Optional[QuestStatusEnum] = None
    max_participants: Optional[int] = Field(None, ge=1, le=1000)
    min_participants: Optional[int] = Field(None, ge=1)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    estimated_duration: Optional[int] = Field(None, ge=1)
    points_reward: Optional[int] = Field(None, ge=0)
    quest_data: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = Field(None, max_length=500)


class Quest(QuestBase, UUIDSchema, TimestampSchema):
    status: QuestStatusEnum
    city_id: str
    creator_id: str
    city: Optional[City] = None
    creator: Optional[UserPublic] = None


class QuestWithDetails(Quest):
    """Quest with additional details like checkpoints and participants."""
    checkpoints: List["QuestCheckpoint"] = []
    participant_count: int = 0


# Quest Checkpoint schemas
class QuestCheckpointBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    order_index: int = Field(..., ge=1)
    is_required: bool = True
    points_value: int = Field(0, ge=0)
    requires_photo: bool = False
    verification_radius: float = Field(50.0, ge=1.0, le=1000.0)
    checkpoint_data: Optional[Dict[str, Any]] = None


class QuestCheckpointCreate(QuestCheckpointBase):
    quest_id: str
    location_id: str


class QuestCheckpointUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    order_index: Optional[int] = Field(None, ge=1)
    is_required: Optional[bool] = None
    points_value: Optional[int] = Field(None, ge=0)
    requires_photo: Optional[bool] = None
    verification_radius: Optional[float] = Field(None, ge=1.0, le=1000.0)
    checkpoint_data: Optional[Dict[str, Any]] = None


class QuestCheckpoint(QuestCheckpointBase, UUIDSchema, TimestampSchema):
    quest_id: str
    location_id: str
    location: Optional[Location] = None


# Quest Progress schemas
class QuestProgressBase(BaseSchema):
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    verified_latitude: Optional[float] = Field(None, ge=-90, le=90)
    verified_longitude: Optional[float] = Field(None, ge=-180, le=180)
    verification_photo_url: Optional[str] = Field(None, max_length=500)
    points_earned: int = Field(0, ge=0)
    progress_data: Optional[Dict[str, Any]] = None


class QuestProgressCreate(QuestProgressBase):
    user_id: str
    quest_id: str
    checkpoint_id: Optional[str] = None


class QuestProgressUpdate(BaseSchema):
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
    verified_latitude: Optional[float] = Field(None, ge=-90, le=90)
    verified_longitude: Optional[float] = Field(None, ge=-180, le=180)
    verification_photo_url: Optional[str] = Field(None, max_length=500)
    points_earned: Optional[int] = Field(None, ge=0)
    progress_data: Optional[Dict[str, Any]] = None


class QuestProgress(QuestProgressBase, UUIDSchema, TimestampSchema):
    user_id: str
    quest_id: str
    checkpoint_id: Optional[str]
    checkpoint: Optional[QuestCheckpoint] = None


# Group schemas
class GroupBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_public: bool = True
    max_members: int = Field(50, ge=1, le=1000)
    image_url: Optional[str] = Field(None, max_length=500)
    group_data: Optional[Dict[str, Any]] = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_public: Optional[bool] = None
    max_members: Optional[int] = Field(None, ge=1, le=1000)
    image_url: Optional[str] = Field(None, max_length=500)
    group_data: Optional[Dict[str, Any]] = None


class Group(GroupBase, UUIDSchema, TimestampSchema):
    creator_id: str
    is_active: bool
    creator: Optional[UserPublic] = None
    member_count: Optional[int] = 0


# Achievement schemas
class AchievementBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=50)
    difficulty: str = Field(..., regex="^(easy|medium|hard|legendary)$")
    requirements: Dict[str, Any]
    points_reward: int = Field(0, ge=0)
    badge_url: Optional[str] = Field(None, max_length=500)
    is_active: bool = True
    is_hidden: bool = False


class AchievementCreate(AchievementBase):
    pass


class AchievementUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    difficulty: Optional[str] = Field(None, regex="^(easy|medium|hard|legendary)$")
    requirements: Optional[Dict[str, Any]] = None
    points_reward: Optional[int] = Field(None, ge=0)
    badge_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None
    is_hidden: Optional[bool] = None


class Achievement(AchievementBase, UUIDSchema, TimestampSchema):
    pass


# User Achievement schemas
class UserAchievementBase(BaseSchema):
    progress: float = Field(0.0, ge=0.0, le=1.0)
    is_completed: bool = False
    completed_at: Optional[datetime] = None


class UserAchievement(UserAchievementBase, UUIDSchema, TimestampSchema):
    user_id: str
    achievement_id: str
    achievement: Optional[Achievement] = None


# Friendship schemas
class FriendshipBase(BaseSchema):
    status: FriendshipStatusEnum


class FriendshipCreate(BaseSchema):
    addressee_id: str


class Friendship(FriendshipBase, UUIDSchema, TimestampSchema):
    requester_id: str
    addressee_id: str
    requested_at: datetime
    responded_at: Optional[datetime]
    requester: Optional[UserPublic] = None
    addressee: Optional[UserPublic] = None


# Authentication schemas
class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseSchema):
    user_id: Optional[str] = None
    email: Optional[str] = None


class LoginRequest(BaseSchema):
    email: EmailStr
    password: str


class RegisterRequest(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


# Update forward references
QuestWithDetails.model_rebuild()