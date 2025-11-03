"""Core database models for the Seeker platform."""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, 
    ForeignKey, Table, Enum, JSON, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class UUIDMixin:
    """Mixin for UUID primary key."""
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)


# Enums
class QuestStatus(enum.Enum):
    """Quest status enumeration."""
    DRAFT = "draft"
    UPCOMING = "upcoming"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class QuestDifficulty(enum.Enum):
    """Quest difficulty enumeration."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class GroupRole(enum.Enum):
    """Group member role enumeration."""
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    OWNER = "owner"


class FriendshipStatus(enum.Enum):
    """Friendship status enumeration."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"


# Association tables for many-to-many relationships
quest_participants = Table(
    'quest_participants',
    Base.metadata,
    Column('quest_id', UUID(as_uuid=True), ForeignKey('quests.id'), primary_key=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('joined_at', DateTime(timezone=True), server_default=func.now()),
    Column('completed_at', DateTime(timezone=True), nullable=True),
    Column('is_active', Boolean, default=True)
)

group_members = Table(
    'group_members',
    Base.metadata,
    Column('group_id', UUID(as_uuid=True), ForeignKey('groups.id'), primary_key=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('role', Enum(GroupRole), default=GroupRole.MEMBER),
    Column('joined_at', DateTime(timezone=True), server_default=func.now()),
    Column('is_active', Boolean, default=True)
)


# Core Models
class User(Base, UUIDMixin, TimestampMixin):
    """User model."""
    __tablename__ = 'users'

    # Basic information
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    display_name = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Status and preferences
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Location preferences
    preferred_city_id = Column(UUID(as_uuid=True), ForeignKey('cities.id'), nullable=True)
    
    # Privacy settings
    profile_visibility = Column(String(20), default='public')  # public, friends, private
    location_sharing = Column(Boolean, default=True)
    
    # OAuth information
    google_id = Column(String(100), nullable=True, unique=True)
    apple_id = Column(String(100), nullable=True, unique=True)
    
    # Relationships
    preferred_city = relationship("City", back_populates="preferred_by_users")
    quest_participations = relationship("Quest", secondary=quest_participants, back_populates="participants")
    group_memberships = relationship("Group", secondary=group_members, back_populates="members")
    created_quests = relationship("Quest", back_populates="creator", foreign_keys="Quest.creator_id")
    created_groups = relationship("Group", back_populates="creator")
    user_stats = relationship("UserStats", back_populates="user", uselist=False)
    rewards = relationship("UserReward", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    quest_progress = relationship("QuestProgress", back_populates="user")
    
    # Friendship relationships
    sent_friend_requests = relationship(
        "Friendship", 
        foreign_keys="Friendship.requester_id",
        back_populates="requester"
    )
    received_friend_requests = relationship(
        "Friendship", 
        foreign_keys="Friendship.addressee_id",
        back_populates="addressee"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class City(Base, UUIDMixin, TimestampMixin):
    """City model for quest locations."""
    __tablename__ = 'cities'

    name = Column(String(100), nullable=False, index=True)
    country = Column(String(100), nullable=False, index=True)
    state_province = Column(String(100), nullable=True)
    
    # Geographic coordinates
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Additional information
    timezone = Column(String(50), nullable=True)
    population = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    metadata = Column(JSON, nullable=True)  # For additional city-specific data
    
    # Relationships
    quests = relationship("Quest", back_populates="city")
    preferred_by_users = relationship("User", back_populates="preferred_city")
    locations = relationship("Location", back_populates="city")

    # Indexes
    __table_args__ = (
        Index('idx_city_coordinates', 'latitude', 'longitude'),
        Index('idx_city_location', 'name', 'country'),
    )

    def __repr__(self):
        return f"<City(id={self.id}, name={self.name}, country={self.country})>"


class Location(Base, UUIDMixin, TimestampMixin):
    """Specific locations within cities for quests."""
    __tablename__ = 'locations'

    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Geographic coordinates
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    radius = Column(Float, default=50.0)  # Radius in meters for location verification
    
    # Address information
    address = Column(String(500), nullable=True)
    
    # Relationships
    city_id = Column(UUID(as_uuid=True), ForeignKey('cities.id'), nullable=False)
    city = relationship("City", back_populates="locations")
    quest_checkpoints = relationship("QuestCheckpoint", back_populates="location")

    # Indexes
    __table_args__ = (
        Index('idx_location_coordinates', 'latitude', 'longitude'),
    )

    def __repr__(self):
        return f"<Location(id={self.id}, name={self.name})>"


class Quest(Base, UUIDMixin, TimestampMixin):
    """Quest model."""
    __tablename__ = 'quests'

    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    short_description = Column(String(500), nullable=True)
    
    # Quest properties
    difficulty = Column(Enum(QuestDifficulty), nullable=False, index=True)
    status = Column(Enum(QuestStatus), default=QuestStatus.DRAFT, nullable=False, index=True)
    
    # Capacity and participation
    max_participants = Column(Integer, default=50, nullable=False)
    min_participants = Column(Integer, default=1, nullable=False)
    
    # Timing
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    estimated_duration = Column(Integer, nullable=True)  # Duration in minutes
    
    # Rewards
    points_reward = Column(Integer, default=0, nullable=False)
    
    # Location
    city_id = Column(UUID(as_uuid=True), ForeignKey('cities.id'), nullable=False)
    
    # Creator
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Quest data
    quest_data = Column(JSON, nullable=True)  # Flexible data for quest-specific information
    
    # Media
    image_url = Column(String(500), nullable=True)
    
    # Relationships
    city = relationship("City", back_populates="quests")
    creator = relationship("User", back_populates="created_quests", foreign_keys=[creator_id])
    participants = relationship("User", secondary=quest_participants, back_populates="quest_participations")
    checkpoints = relationship("QuestCheckpoint", back_populates="quest", cascade="all, delete-orphan")
    progress_records = relationship("QuestProgress", back_populates="quest", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_quest_city_status', 'city_id', 'status'),
        Index('idx_quest_timing', 'start_time', 'end_time'),
    )

    def __repr__(self):
        return f"<Quest(id={self.id}, title={self.title}, status={self.status})>"


class QuestCheckpoint(Base, UUIDMixin, TimestampMixin):
    """Quest checkpoint model for location-based objectives."""
    __tablename__ = 'quest_checkpoints'

    quest_id = Column(UUID(as_uuid=True), ForeignKey('quests.id'), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id'), nullable=False)
    
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)  # Order of checkpoint in quest
    
    # Checkpoint properties
    is_required = Column(Boolean, default=True, nullable=False)
    points_value = Column(Integer, default=0, nullable=False)
    
    # Verification requirements
    requires_photo = Column(Boolean, default=False, nullable=False)
    verification_radius = Column(Float, default=50.0, nullable=False)  # Meters
    
    # Checkpoint data
    checkpoint_data = Column(JSON, nullable=True)
    
    # Relationships
    quest = relationship("Quest", back_populates="checkpoints")
    location = relationship("Location", back_populates="quest_checkpoints")
    progress_records = relationship("QuestProgress", back_populates="checkpoint")

    # Indexes
    __table_args__ = (
        Index('idx_checkpoint_quest_order', 'quest_id', 'order_index'),
    )

    def __repr__(self):
        return f"<QuestCheckpoint(id={self.id}, name={self.name})>"


class QuestProgress(Base, UUIDMixin, TimestampMixin):
    """Quest progress tracking model."""
    __tablename__ = 'quest_progress'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    quest_id = Column(UUID(as_uuid=True), ForeignKey('quests.id'), nullable=False)
    checkpoint_id = Column(UUID(as_uuid=True), ForeignKey('quest_checkpoints.id'), nullable=True)
    
    # Progress information
    is_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Location verification
    verified_latitude = Column(Float, nullable=True)
    verified_longitude = Column(Float, nullable=True)
    verification_photo_url = Column(String(500), nullable=True)
    
    # Points earned
    points_earned = Column(Integer, default=0, nullable=False)
    
    # Progress data
    progress_data = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="quest_progress")
    quest = relationship("Quest", back_populates="progress_records")
    checkpoint = relationship("QuestCheckpoint", back_populates="progress_records")

    # Indexes
    __table_args__ = (
        Index('idx_progress_user_quest', 'user_id', 'quest_id'),
        Index('idx_progress_completion', 'is_completed', 'completed_at'),
    )

    def __repr__(self):
        return f"<QuestProgress(user_id={self.user_id}, quest_id={self.quest_id})>"


class Group(Base, UUIDMixin, TimestampMixin):
    """Group model for social features."""
    __tablename__ = 'groups'

    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Group properties
    is_public = Column(Boolean, default=True, nullable=False)
    max_members = Column(Integer, default=50, nullable=False)
    
    # Creator
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Group image
    image_url = Column(String(500), nullable=True)
    
    # Group data
    group_data = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    creator = relationship("User", back_populates="created_groups")
    members = relationship("User", secondary=group_members, back_populates="group_memberships")

    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name})>"


class UserStats(Base, UUIDMixin, TimestampMixin):
    """User statistics model."""
    __tablename__ = 'user_stats'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, unique=True)
    
    # Quest statistics
    quests_completed = Column(Integer, default=0, nullable=False)
    quests_joined = Column(Integer, default=0, nullable=False)
    quests_created = Column(Integer, default=0, nullable=False)
    
    # Points and rewards
    total_points = Column(Integer, default=0, nullable=False)
    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    
    # Social statistics
    friends_count = Column(Integer, default=0, nullable=False)
    groups_joined = Column(Integer, default=0, nullable=False)
    groups_created = Column(Integer, default=0, nullable=False)
    
    # Activity statistics
    last_activity_at = Column(DateTime(timezone=True), nullable=True)
    total_distance_traveled = Column(Float, default=0.0, nullable=False)  # In kilometers
    
    # Relationships
    user = relationship("User", back_populates="user_stats")

    def __repr__(self):
        return f"<UserStats(user_id={self.user_id}, total_points={self.total_points})>"


class UserReward(Base, UUIDMixin, TimestampMixin):
    """User reward model."""
    __tablename__ = 'user_rewards'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Reward information
    reward_type = Column(String(50), nullable=False)  # points, badge, item, etc.
    reward_name = Column(String(200), nullable=False)
    reward_description = Column(Text, nullable=True)
    
    # Reward value
    points_value = Column(Integer, default=0, nullable=False)
    
    # Source information
    source_type = Column(String(50), nullable=False)  # quest, achievement, bonus, etc.
    source_id = Column(UUID(as_uuid=True), nullable=True)  # ID of the source (quest, achievement, etc.)
    
    # Status
    is_claimed = Column(Boolean, default=False, nullable=False)
    claimed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Reward data
    reward_data = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="rewards")

    # Indexes
    __table_args__ = (
        Index('idx_reward_user_type', 'user_id', 'reward_type'),
        Index('idx_reward_source', 'source_type', 'source_id'),
    )

    def __repr__(self):
        return f"<UserReward(user_id={self.user_id}, reward_name={self.reward_name})>"


class Achievement(Base, UUIDMixin, TimestampMixin):
    """Achievement definition model."""
    __tablename__ = 'achievements'

    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    
    # Achievement properties
    category = Column(String(50), nullable=False, index=True)
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard, legendary
    
    # Requirements
    requirements = Column(JSON, nullable=False)  # Flexible requirements definition
    
    # Rewards
    points_reward = Column(Integer, default=0, nullable=False)
    badge_url = Column(String(500), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_hidden = Column(Boolean, default=False, nullable=False)  # Hidden until unlocked
    
    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")

    def __repr__(self):
        return f"<Achievement(id={self.id}, name={self.name})>"


class UserAchievement(Base, UUIDMixin, TimestampMixin):
    """User achievement model."""
    __tablename__ = 'user_achievements'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    achievement_id = Column(UUID(as_uuid=True), ForeignKey('achievements.id'), nullable=False)
    
    # Achievement progress
    progress = Column(Float, default=0.0, nullable=False)  # Progress percentage (0.0 to 1.0)
    is_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")

    # Indexes
    __table_args__ = (
        Index('idx_user_achievement', 'user_id', 'achievement_id'),
        Index('idx_achievement_completion', 'is_completed', 'completed_at'),
    )

    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id})>"


class Friendship(Base, UUIDMixin, TimestampMixin):
    """Friendship model."""
    __tablename__ = 'friendships'

    requester_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    addressee_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    status = Column(Enum(FriendshipStatus), default=FriendshipStatus.PENDING, nullable=False)
    
    # Timestamps
    requested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    responded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    requester = relationship("User", foreign_keys=[requester_id], back_populates="sent_friend_requests")
    addressee = relationship("User", foreign_keys=[addressee_id], back_populates="received_friend_requests")

    # Indexes
    __table_args__ = (
        Index('idx_friendship_users', 'requester_id', 'addressee_id'),
        Index('idx_friendship_status', 'status'),
    )

    def __repr__(self):
        return f"<Friendship(requester_id={self.requester_id}, addressee_id={self.addressee_id}, status={self.status})>"