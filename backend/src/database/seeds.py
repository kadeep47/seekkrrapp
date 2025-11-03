"""Database seeding scripts for development data."""

import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .models import (
    User, City, Location, Quest, QuestCheckpoint, Group, Achievement,
    UserStats, QuestStatus, QuestDifficulty, GroupRole
)
from .config import SessionLocal

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def seed_cities(db: Session) -> list[City]:
    """Seed cities data."""
    cities_data = [
        {
            "name": "San Francisco",
            "country": "United States",
            "state_province": "California",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "timezone": "America/Los_Angeles",
            "population": 873965,
            "description": "The cultural, commercial, and financial center of Northern California."
        },
        {
            "name": "New York",
            "country": "United States", 
            "state_province": "New York",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York",
            "population": 8336817,
            "description": "The most populous city in the United States."
        },
        {
            "name": "London",
            "country": "United Kingdom",
            "state_province": "England",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "timezone": "Europe/London",
            "population": 9648110,
            "description": "The capital and largest city of England and the United Kingdom."
        },
        {
            "name": "Tokyo",
            "country": "Japan",
            "state_province": "Tokyo",
            "latitude": 35.6762,
            "longitude": 139.6503,
            "timezone": "Asia/Tokyo",
            "population": 37400068,
            "description": "The capital of Japan and the most populous metropolitan area in the world."
        },
        {
            "name": "Paris",
            "country": "France",
            "state_province": "Île-de-France",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "timezone": "Europe/Paris",
            "population": 2161000,
            "description": "The capital and most populous city of France."
        }
    ]
    
    cities = []
    for city_data in cities_data:
        city = City(**city_data)
        db.add(city)
        cities.append(city)
    
    db.commit()
    return cities


def seed_locations(db: Session, cities: list[City]) -> list[Location]:
    """Seed locations data."""
    locations_data = [
        # San Francisco locations
        {
            "name": "Golden Gate Bridge",
            "description": "Iconic suspension bridge spanning the Golden Gate strait",
            "latitude": 37.8199,
            "longitude": -122.4783,
            "address": "Golden Gate Bridge, San Francisco, CA",
            "city": cities[0]  # San Francisco
        },
        {
            "name": "Fisherman's Wharf",
            "description": "Popular tourist attraction and working wharf",
            "latitude": 37.8080,
            "longitude": -122.4177,
            "address": "Fisherman's Wharf, San Francisco, CA",
            "city": cities[0]
        },
        {
            "name": "Alcatraz Island",
            "description": "Former federal prison on an island",
            "latitude": 37.8267,
            "longitude": -122.4233,
            "address": "Alcatraz Island, San Francisco, CA",
            "city": cities[0]
        },
        # New York locations
        {
            "name": "Times Square",
            "description": "Major commercial intersection and tourist destination",
            "latitude": 40.7580,
            "longitude": -73.9855,
            "address": "Times Square, New York, NY",
            "city": cities[1]  # New York
        },
        {
            "name": "Central Park",
            "description": "Large public park in Manhattan",
            "latitude": 40.7829,
            "longitude": -73.9654,
            "address": "Central Park, New York, NY",
            "city": cities[1]
        },
        {
            "name": "Statue of Liberty",
            "description": "Neoclassical sculpture on Liberty Island",
            "latitude": 40.6892,
            "longitude": -74.0445,
            "address": "Liberty Island, New York, NY",
            "city": cities[1]
        },
        # London locations
        {
            "name": "Big Ben",
            "description": "Famous clock tower at the Palace of Westminster",
            "latitude": 51.4994,
            "longitude": -0.1245,
            "address": "Westminster, London, UK",
            "city": cities[2]  # London
        },
        {
            "name": "Tower Bridge",
            "description": "Victorian Gothic bascule bridge",
            "latitude": 51.5055,
            "longitude": -0.0754,
            "address": "Tower Bridge Rd, London, UK",
            "city": cities[2]
        },
        {
            "name": "London Eye",
            "description": "Giant observation wheel on the South Bank",
            "latitude": 51.5033,
            "longitude": -0.1196,
            "address": "Riverside Building, County Hall, London, UK",
            "city": cities[2]
        }
    ]
    
    locations = []
    for location_data in locations_data:
        location = Location(**location_data)
        db.add(location)
        locations.append(location)
    
    db.commit()
    return locations


def seed_users(db: Session, cities: list[City]) -> list[User]:
    """Seed users data."""
    users_data = [
        {
            "email": "admin@seeker.com",
            "username": "admin",
            "password_hash": hash_password("admin123"),
            "first_name": "Admin",
            "last_name": "User",
            "display_name": "Admin",
            "bio": "Platform administrator",
            "is_active": True,
            "is_verified": True,
            "email_verified_at": datetime.utcnow(),
            "preferred_city": cities[0],  # San Francisco
            "profile_visibility": "public",
            "location_sharing": True
        },
        {
            "email": "john.doe@example.com",
            "username": "johndoe",
            "password_hash": hash_password("password123"),
            "first_name": "John",
            "last_name": "Doe",
            "display_name": "John D.",
            "bio": "Adventure seeker and quest enthusiast",
            "is_active": True,
            "is_verified": True,
            "email_verified_at": datetime.utcnow(),
            "preferred_city": cities[1],  # New York
            "profile_visibility": "public",
            "location_sharing": True
        },
        {
            "email": "jane.smith@example.com",
            "username": "janesmith",
            "password_hash": hash_password("password123"),
            "first_name": "Jane",
            "last_name": "Smith",
            "display_name": "Jane S.",
            "bio": "Explorer and photographer",
            "is_active": True,
            "is_verified": True,
            "email_verified_at": datetime.utcnow(),
            "preferred_city": cities[2],  # London
            "profile_visibility": "public",
            "location_sharing": True
        },
        {
            "email": "mike.wilson@example.com",
            "username": "mikewilson",
            "password_hash": hash_password("password123"),
            "first_name": "Mike",
            "last_name": "Wilson",
            "display_name": "Mike W.",
            "bio": "Urban explorer and team player",
            "is_active": True,
            "is_verified": True,
            "email_verified_at": datetime.utcnow(),
            "preferred_city": cities[0],  # San Francisco
            "profile_visibility": "friends",
            "location_sharing": False
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
        users.append(user)
    
    db.commit()
    
    # Create user stats for each user
    for user in users:
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
        db.add(user_stats)
    
    db.commit()
    return users


def seed_achievements(db: Session) -> list[Achievement]:
    """Seed achievements data."""
    achievements_data = [
        {
            "name": "First Steps",
            "description": "Complete your first quest",
            "category": "beginner",
            "difficulty": "easy",
            "requirements": {"quests_completed": 1},
            "points_reward": 100,
            "is_active": True,
            "is_hidden": False
        },
        {
            "name": "Explorer",
            "description": "Complete 10 quests",
            "category": "progress",
            "difficulty": "medium",
            "requirements": {"quests_completed": 10},
            "points_reward": 500,
            "is_active": True,
            "is_hidden": False
        },
        {
            "name": "Quest Master",
            "description": "Complete 50 quests",
            "category": "progress",
            "difficulty": "hard",
            "requirements": {"quests_completed": 50},
            "points_reward": 2000,
            "is_active": True,
            "is_hidden": False
        },
        {
            "name": "Social Butterfly",
            "description": "Join 5 groups",
            "category": "social",
            "difficulty": "easy",
            "requirements": {"groups_joined": 5},
            "points_reward": 200,
            "is_active": True,
            "is_hidden": False
        },
        {
            "name": "City Explorer",
            "description": "Complete quests in 3 different cities",
            "category": "exploration",
            "difficulty": "medium",
            "requirements": {"cities_visited": 3},
            "points_reward": 750,
            "is_active": True,
            "is_hidden": False
        },
        {
            "name": "Legendary Seeker",
            "description": "Reach 10,000 total points",
            "category": "legendary",
            "difficulty": "legendary",
            "requirements": {"total_points": 10000},
            "points_reward": 5000,
            "is_active": True,
            "is_hidden": True
        }
    ]
    
    achievements = []
    for achievement_data in achievements_data:
        achievement = Achievement(**achievement_data)
        db.add(achievement)
        achievements.append(achievement)
    
    db.commit()
    return achievements


def seed_quests(db: Session, users: list[User], cities: list[City], locations: list[Location]) -> list[Quest]:
    """Seed quests data."""
    quests_data = [
        {
            "title": "Golden Gate Adventure",
            "description": "Explore the iconic landmarks of San Francisco including the Golden Gate Bridge and Fisherman's Wharf",
            "short_description": "Discover San Francisco's most famous attractions",
            "difficulty": QuestDifficulty.EASY,
            "status": QuestStatus.ACTIVE,
            "max_participants": 20,
            "min_participants": 1,
            "start_time": datetime.utcnow() - timedelta(days=1),
            "end_time": datetime.utcnow() + timedelta(days=30),
            "estimated_duration": 180,  # 3 hours
            "points_reward": 300,
            "city": cities[0],  # San Francisco
            "creator": users[0],  # Admin
            "quest_data": {
                "theme": "sightseeing",
                "tags": ["landmarks", "photography", "walking"]
            }
        },
        {
            "title": "NYC Urban Explorer",
            "description": "Navigate through the bustling streets of New York City and visit Times Square, Central Park, and the Statue of Liberty",
            "short_description": "Experience the best of New York City",
            "difficulty": QuestDifficulty.MEDIUM,
            "status": QuestStatus.UPCOMING,
            "max_participants": 15,
            "min_participants": 2,
            "start_time": datetime.utcnow() + timedelta(days=7),
            "end_time": datetime.utcnow() + timedelta(days=37),
            "estimated_duration": 240,  # 4 hours
            "points_reward": 500,
            "city": cities[1],  # New York
            "creator": users[1],  # John Doe
            "quest_data": {
                "theme": "urban_exploration",
                "tags": ["city", "landmarks", "culture"]
            }
        },
        {
            "title": "London Historical Journey",
            "description": "Step back in time and explore London's rich history through Big Ben, Tower Bridge, and the London Eye",
            "short_description": "Discover London's historical treasures",
            "difficulty": QuestDifficulty.MEDIUM,
            "status": QuestStatus.ACTIVE,
            "max_participants": 25,
            "min_participants": 1,
            "start_time": datetime.utcnow() - timedelta(days=3),
            "end_time": datetime.utcnow() + timedelta(days=27),
            "estimated_duration": 300,  # 5 hours
            "points_reward": 600,
            "city": cities[2],  # London
            "creator": users[2],  # Jane Smith
            "quest_data": {
                "theme": "history",
                "tags": ["historical", "architecture", "culture"]
            }
        }
    ]
    
    quests = []
    for quest_data in quests_data:
        quest = Quest(**quest_data)
        db.add(quest)
        quests.append(quest)
    
    db.commit()
    
    # Create checkpoints for each quest
    quest_checkpoints = [
        # Golden Gate Adventure checkpoints
        [
            {
                "quest": quests[0],
                "location": locations[0],  # Golden Gate Bridge
                "name": "Golden Gate Bridge Photo",
                "description": "Take a photo at the Golden Gate Bridge",
                "order_index": 1,
                "is_required": True,
                "points_value": 100,
                "requires_photo": True,
                "verification_radius": 100.0
            },
            {
                "quest": quests[0],
                "location": locations[1],  # Fisherman's Wharf
                "name": "Fisherman's Wharf Visit",
                "description": "Explore Fisherman's Wharf and its attractions",
                "order_index": 2,
                "is_required": True,
                "points_value": 100,
                "requires_photo": False,
                "verification_radius": 150.0
            },
            {
                "quest": quests[0],
                "location": locations[2],  # Alcatraz Island
                "name": "Alcatraz View",
                "description": "Get a view of Alcatraz Island",
                "order_index": 3,
                "is_required": False,
                "points_value": 100,
                "requires_photo": True,
                "verification_radius": 200.0
            }
        ],
        # NYC Urban Explorer checkpoints
        [
            {
                "quest": quests[1],
                "location": locations[3],  # Times Square
                "name": "Times Square Experience",
                "description": "Experience the energy of Times Square",
                "order_index": 1,
                "is_required": True,
                "points_value": 150,
                "requires_photo": True,
                "verification_radius": 100.0
            },
            {
                "quest": quests[1],
                "location": locations[4],  # Central Park
                "name": "Central Park Stroll",
                "description": "Take a peaceful walk through Central Park",
                "order_index": 2,
                "is_required": True,
                "points_value": 150,
                "requires_photo": False,
                "verification_radius": 200.0
            },
            {
                "quest": quests[1],
                "location": locations[5],  # Statue of Liberty
                "name": "Liberty Island Visit",
                "description": "Visit the Statue of Liberty",
                "order_index": 3,
                "is_required": True,
                "points_value": 200,
                "requires_photo": True,
                "verification_radius": 150.0
            }
        ],
        # London Historical Journey checkpoints
        [
            {
                "quest": quests[2],
                "location": locations[6],  # Big Ben
                "name": "Big Ben Clock Tower",
                "description": "Visit the famous Big Ben clock tower",
                "order_index": 1,
                "is_required": True,
                "points_value": 200,
                "requires_photo": True,
                "verification_radius": 100.0
            },
            {
                "quest": quests[2],
                "location": locations[7],  # Tower Bridge
                "name": "Tower Bridge Crossing",
                "description": "Cross the historic Tower Bridge",
                "order_index": 2,
                "is_required": True,
                "points_value": 200,
                "requires_photo": True,
                "verification_radius": 100.0
            },
            {
                "quest": quests[2],
                "location": locations[8],  # London Eye
                "name": "London Eye View",
                "description": "Enjoy the view from the London Eye area",
                "order_index": 3,
                "is_required": False,
                "points_value": 200,
                "requires_photo": False,
                "verification_radius": 150.0
            }
        ]
    ]
    
    for quest_checkpoint_list in quest_checkpoints:
        for checkpoint_data in quest_checkpoint_list:
            checkpoint = QuestCheckpoint(**checkpoint_data)
            db.add(checkpoint)
    
    db.commit()
    return quests


def seed_groups(db: Session, users: list[User]) -> list[Group]:
    """Seed groups data."""
    groups_data = [
        {
            "name": "San Francisco Explorers",
            "description": "A group for people who love exploring San Francisco",
            "is_public": True,
            "max_members": 50,
            "creator": users[0],  # Admin
            "is_active": True,
            "group_data": {
                "focus": "local_exploration",
                "meeting_frequency": "weekly"
            }
        },
        {
            "name": "Photography Enthusiasts",
            "description": "For those who love capturing moments during quests",
            "is_public": True,
            "max_members": 30,
            "creator": users[2],  # Jane Smith
            "is_active": True,
            "group_data": {
                "focus": "photography",
                "skill_level": "all_levels"
            }
        },
        {
            "name": "Weekend Warriors",
            "description": "Active group for weekend quest adventures",
            "is_public": False,
            "max_members": 20,
            "creator": users[1],  # John Doe
            "is_active": True,
            "group_data": {
                "focus": "weekend_activities",
                "activity_level": "high"
            }
        }
    ]
    
    groups = []
    for group_data in groups_data:
        group = Group(**group_data)
        db.add(group)
        groups.append(group)
    
    db.commit()
    return groups


def seed_database():
    """Seed the database with development data."""
    db = SessionLocal()
    
    try:
        print("Seeding cities...")
        cities = seed_cities(db)
        
        print("Seeding locations...")
        locations = seed_locations(db, cities)
        
        print("Seeding users...")
        users = seed_users(db, cities)
        
        print("Seeding achievements...")
        achievements = seed_achievements(db)
        
        print("Seeding quests...")
        quests = seed_quests(db, users, cities, locations)
        
        print("Seeding groups...")
        groups = seed_groups(db, users)
        
        print("Database seeding completed successfully!")
        
        return {
            "cities": len(cities),
            "locations": len(locations),
            "users": len(users),
            "achievements": len(achievements),
            "quests": len(quests),
            "groups": len(groups)
        }
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    result = seed_database()
    print(f"Seeded: {result}")