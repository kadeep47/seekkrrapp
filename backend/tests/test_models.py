"""Tests for database models."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.models import (
    Base, User, City, Location, Quest, QuestCheckpoint, Group, 
    UserStats, Achievement, QuestStatus, QuestDifficulty
)

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
def sample_city(db_session):
    """Create a sample city for testing."""
    city = City(
        name="Test City",
        country="Test Country",
        latitude=37.7749,
        longitude=-122.4194,
        is_active=True
    )
    db_session.add(city)
    db_session.commit()
    db_session.refresh(city)
    return city


@pytest.fixture
def sample_user(db_session, sample_city):
    """Create a sample user for testing."""
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password",
        first_name="Test",
        last_name="User",
        is_active=True,
        is_verified=True,
        preferred_city_id=sample_city.id
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_city_creation(db_session):
    """Test city model creation."""
    city = City(
        name="San Francisco",
        country="United States",
        state_province="California",
        latitude=37.7749,
        longitude=-122.4194,
        timezone="America/Los_Angeles",
        population=873965,
        is_active=True
    )
    
    db_session.add(city)
    db_session.commit()
    db_session.refresh(city)
    
    assert city.id is not None
    assert city.name == "San Francisco"
    assert city.country == "United States"
    assert city.latitude == 37.7749
    assert city.longitude == -122.4194
    assert city.is_active is True
    assert city.created_at is not None
    assert city.updated_at is not None


def test_user_creation(db_session, sample_city):
    """Test user model creation."""
    user = User(
        email="john.doe@example.com",
        username="johndoe",
        password_hash="hashed_password_123",
        first_name="John",
        last_name="Doe",
        display_name="John D.",
        bio="Test user bio",
        is_active=True,
        is_verified=False,
        preferred_city_id=sample_city.id,
        profile_visibility="public",
        location_sharing=True
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.id is not None
    assert user.email == "john.doe@example.com"
    assert user.username == "johndoe"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.is_active is True
    assert user.is_verified is False
    assert user.preferred_city_id == sample_city.id
    assert user.created_at is not None


def test_user_city_relationship(db_session, sample_user, sample_city):
    """Test user-city relationship."""
    assert sample_user.preferred_city is not None
    assert sample_user.preferred_city.id == sample_city.id
    assert sample_user.preferred_city.name == sample_city.name


def test_location_creation(db_session, sample_city):
    """Test location model creation."""
    location = Location(
        name="Golden Gate Bridge",
        description="Famous suspension bridge",
        latitude=37.8199,
        longitude=-122.4783,
        radius=100.0,
        address="Golden Gate Bridge, San Francisco, CA",
        city_id=sample_city.id
    )
    
    db_session.add(location)
    db_session.commit()
    db_session.refresh(location)
    
    assert location.id is not None
    assert location.name == "Golden Gate Bridge"
    assert location.city_id == sample_city.id
    assert location.radius == 100.0
    assert location.created_at is not None


def test_quest_creation(db_session, sample_user, sample_city):
    """Test quest model creation."""
    quest = Quest(
        title="Test Quest",
        description="A test quest for unit testing",
        short_description="Test quest",
        difficulty=QuestDifficulty.EASY,
        status=QuestStatus.DRAFT,
        max_participants=20,
        min_participants=1,
        start_time=datetime.utcnow() + timedelta(days=1),
        end_time=datetime.utcnow() + timedelta(days=8),
        estimated_duration=120,
        points_reward=100,
        city_id=sample_city.id,
        creator_id=sample_user.id
    )
    
    db_session.add(quest)
    db_session.commit()
    db_session.refresh(quest)
    
    assert quest.id is not None
    assert quest.title == "Test Quest"
    assert quest.difficulty == QuestDifficulty.EASY
    assert quest.status == QuestStatus.DRAFT
    assert quest.max_participants == 20
    assert quest.points_reward == 100
    assert quest.city_id == sample_city.id
    assert quest.creator_id == sample_user.id
    assert quest.created_at is not None


def test_quest_relationships(db_session, sample_user, sample_city):
    """Test quest relationships."""
    quest = Quest(
        title="Relationship Test Quest",
        description="Testing relationships",
        difficulty=QuestDifficulty.MEDIUM,
        status=QuestStatus.ACTIVE,
        max_participants=10,
        min_participants=1,
        points_reward=200,
        city_id=sample_city.id,
        creator_id=sample_user.id
    )
    
    db_session.add(quest)
    db_session.commit()
    db_session.refresh(quest)
    
    # Test city relationship
    assert quest.city is not None
    assert quest.city.id == sample_city.id
    assert quest.city.name == sample_city.name
    
    # Test creator relationship
    assert quest.creator is not None
    assert quest.creator.id == sample_user.id
    assert quest.creator.email == sample_user.email


def test_user_stats_creation(db_session, sample_user):
    """Test user stats model creation."""
    user_stats = UserStats(
        user_id=sample_user.id,
        quests_completed=5,
        quests_joined=10,
        total_points=500,
        current_streak=3,
        longest_streak=7,
        friends_count=2,
        groups_joined=1,
        total_distance_traveled=15.5
    )
    
    db_session.add(user_stats)
    db_session.commit()
    db_session.refresh(user_stats)
    
    assert user_stats.id is not None
    assert user_stats.user_id == sample_user.id
    assert user_stats.quests_completed == 5
    assert user_stats.total_points == 500
    assert user_stats.current_streak == 3
    assert user_stats.total_distance_traveled == 15.5
    assert user_stats.created_at is not None


def test_group_creation(db_session, sample_user):
    """Test group model creation."""
    group = Group(
        name="Test Group",
        description="A test group for unit testing",
        is_public=True,
        max_members=25,
        creator_id=sample_user.id,
        is_active=True
    )
    
    db_session.add(group)
    db_session.commit()
    db_session.refresh(group)
    
    assert group.id is not None
    assert group.name == "Test Group"
    assert group.is_public is True
    assert group.max_members == 25
    assert group.creator_id == sample_user.id
    assert group.is_active is True
    assert group.created_at is not None


def test_achievement_creation(db_session):
    """Test achievement model creation."""
    achievement = Achievement(
        name="Test Achievement",
        description="A test achievement",
        category="testing",
        difficulty="easy",
        requirements={"quests_completed": 1},
        points_reward=100,
        is_active=True,
        is_hidden=False
    )
    
    db_session.add(achievement)
    db_session.commit()
    db_session.refresh(achievement)
    
    assert achievement.id is not None
    assert achievement.name == "Test Achievement"
    assert achievement.category == "testing"
    assert achievement.difficulty == "easy"
    assert achievement.requirements == {"quests_completed": 1}
    assert achievement.points_reward == 100
    assert achievement.is_active is True
    assert achievement.created_at is not None


def test_quest_checkpoint_creation(db_session, sample_city, sample_user):
    """Test quest checkpoint model creation."""
    # Create a quest first
    quest = Quest(
        title="Checkpoint Test Quest",
        description="Testing checkpoints",
        difficulty=QuestDifficulty.EASY,
        status=QuestStatus.DRAFT,
        max_participants=10,
        min_participants=1,
        points_reward=100,
        city_id=sample_city.id,
        creator_id=sample_user.id
    )
    db_session.add(quest)
    
    # Create a location
    location = Location(
        name="Test Location",
        description="Test location for checkpoint",
        latitude=37.7749,
        longitude=-122.4194,
        city_id=sample_city.id
    )
    db_session.add(location)
    db_session.commit()
    db_session.refresh(quest)
    db_session.refresh(location)
    
    # Create checkpoint
    checkpoint = QuestCheckpoint(
        quest_id=quest.id,
        location_id=location.id,
        name="Test Checkpoint",
        description="A test checkpoint",
        order_index=1,
        is_required=True,
        points_value=50,
        requires_photo=True,
        verification_radius=75.0
    )
    
    db_session.add(checkpoint)
    db_session.commit()
    db_session.refresh(checkpoint)
    
    assert checkpoint.id is not None
    assert checkpoint.quest_id == quest.id
    assert checkpoint.location_id == location.id
    assert checkpoint.name == "Test Checkpoint"
    assert checkpoint.order_index == 1
    assert checkpoint.is_required is True
    assert checkpoint.points_value == 50
    assert checkpoint.requires_photo is True
    assert checkpoint.verification_radius == 75.0
    assert checkpoint.created_at is not None


def test_model_string_representations(db_session, sample_city, sample_user):
    """Test model __repr__ methods."""
    assert "Test City" in str(sample_city)
    assert "test@example.com" in str(sample_user)
    
    quest = Quest(
        title="Repr Test Quest",
        description="Testing repr",
        difficulty=QuestDifficulty.EASY,
        status=QuestStatus.DRAFT,
        max_participants=10,
        min_participants=1,
        points_reward=100,
        city_id=sample_city.id,
        creator_id=sample_user.id
    )
    db_session.add(quest)
    db_session.commit()
    db_session.refresh(quest)
    
    assert "Repr Test Quest" in str(quest)
    assert "draft" in str(quest)