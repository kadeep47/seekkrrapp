"""Initial database models

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum types
    op.execute("CREATE TYPE queststatus AS ENUM ('draft', 'upcoming', 'active', 'completed', 'cancelled')")
    op.execute("CREATE TYPE questdifficulty AS ENUM ('easy', 'medium', 'hard', 'expert')")
    op.execute("CREATE TYPE grouprole AS ENUM ('member', 'moderator', 'admin', 'owner')")
    op.execute("CREATE TYPE friendshipstatus AS ENUM ('pending', 'accepted', 'blocked')")
    
    # Create cities table
    op.create_table('cities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('country', sa.String(length=100), nullable=False),
        sa.Column('state_province', sa.String(length=100), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('timezone', sa.String(length=50), nullable=True),
        sa.Column('population', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_city_coordinates', 'cities', ['latitude', 'longitude'], unique=False)
    op.create_index('idx_city_location', 'cities', ['name', 'country'], unique=False)
    op.create_index(op.f('ix_cities_country'), 'cities', ['country'], unique=False)
    op.create_index(op.f('ix_cities_name'), 'cities', ['name'], unique=False)

    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('display_name', sa.String(length=100), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('email_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('preferred_city_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('profile_visibility', sa.String(length=20), nullable=True),
        sa.Column('location_sharing', sa.Boolean(), nullable=True),
        sa.Column('google_id', sa.String(length=100), nullable=True),
        sa.Column('apple_id', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['preferred_city_id'], ['cities.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('apple_id'),
        sa.UniqueConstraint('google_id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create locations table
    op.create_table('locations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('radius', sa.Float(), nullable=True),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('city_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_location_coordinates', 'locations', ['latitude', 'longitude'], unique=False)

    # Create achievements table
    op.create_table('achievements',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('difficulty', sa.String(length=20), nullable=False),
        sa.Column('requirements', sa.JSON(), nullable=False),
        sa.Column('points_reward', sa.Integer(), nullable=False),
        sa.Column('badge_url', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_hidden', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_achievements_category'), 'achievements', ['category'], unique=False)

    # Create friendships table
    op.create_table('friendships',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('requester_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('addressee_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.Enum('pending', 'accepted', 'blocked', name='friendshipstatus'), nullable=False),
        sa.Column('requested_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('responded_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['addressee_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['requester_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_friendship_status', 'friendships', ['status'], unique=False)
    op.create_index('idx_friendship_users', 'friendships', ['requester_id', 'addressee_id'], unique=False)

    # Create groups table
    op.create_table('groups',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('max_members', sa.Integer(), nullable=False),
        sa.Column('creator_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('group_data', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groups_name'), 'groups', ['name'], unique=False)

    # Create quests table
    op.create_table('quests',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('short_description', sa.String(length=500), nullable=True),
        sa.Column('difficulty', sa.Enum('easy', 'medium', 'hard', 'expert', name='questdifficulty'), nullable=False),
        sa.Column('status', sa.Enum('draft', 'upcoming', 'active', 'completed', 'cancelled', name='queststatus'), nullable=False),
        sa.Column('max_participants', sa.Integer(), nullable=False),
        sa.Column('min_participants', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('estimated_duration', sa.Integer(), nullable=True),
        sa.Column('points_reward', sa.Integer(), nullable=False),
        sa.Column('city_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('creator_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('quest_data', sa.JSON(), nullable=True),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_quest_city_status', 'quests', ['city_id', 'status'], unique=False)
    op.create_index('idx_quest_timing', 'quests', ['start_time', 'end_time'], unique=False)
    op.create_index(op.f('ix_quests_difficulty'), 'quests', ['difficulty'], unique=False)
    op.create_index(op.f('ix_quests_status'), 'quests', ['status'], unique=False)
    op.create_index(op.f('ix_quests_title'), 'quests', ['title'], unique=False)

    # Create user_achievements table
    op.create_table('user_achievements',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('achievement_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('progress', sa.Float(), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_achievement_completion', 'user_achievements', ['is_completed', 'completed_at'], unique=False)
    op.create_index('idx_user_achievement', 'user_achievements', ['user_id', 'achievement_id'], unique=False)

    # Create user_rewards table
    op.create_table('user_rewards',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('reward_type', sa.String(length=50), nullable=False),
        sa.Column('reward_name', sa.String(length=200), nullable=False),
        sa.Column('reward_description', sa.Text(), nullable=True),
        sa.Column('points_value', sa.Integer(), nullable=False),
        sa.Column('source_type', sa.String(length=50), nullable=False),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_claimed', sa.Boolean(), nullable=False),
        sa.Column('claimed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reward_data', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_reward_source', 'user_rewards', ['source_type', 'source_id'], unique=False)
    op.create_index('idx_reward_user_type', 'user_rewards', ['user_id', 'reward_type'], unique=False)

    # Create user_stats table
    op.create_table('user_stats',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('quests_completed', sa.Integer(), nullable=False),
        sa.Column('quests_joined', sa.Integer(), nullable=False),
        sa.Column('quests_created', sa.Integer(), nullable=False),
        sa.Column('total_points', sa.Integer(), nullable=False),
        sa.Column('current_streak', sa.Integer(), nullable=False),
        sa.Column('longest_streak', sa.Integer(), nullable=False),
        sa.Column('friends_count', sa.Integer(), nullable=False),
        sa.Column('groups_joined', sa.Integer(), nullable=False),
        sa.Column('groups_created', sa.Integer(), nullable=False),
        sa.Column('last_activity_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_distance_traveled', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )

    # Create quest_checkpoints table
    op.create_table('quest_checkpoints',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('quest_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('location_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('is_required', sa.Boolean(), nullable=False),
        sa.Column('points_value', sa.Integer(), nullable=False),
        sa.Column('requires_photo', sa.Boolean(), nullable=False),
        sa.Column('verification_radius', sa.Float(), nullable=False),
        sa.Column('checkpoint_data', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.ForeignKeyConstraint(['quest_id'], ['quests.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_checkpoint_quest_order', 'quest_checkpoints', ['quest_id', 'order_index'], unique=False)

    # Create association tables
    op.create_table('quest_participants',
        sa.Column('quest_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean()),
        sa.ForeignKeyConstraint(['quest_id'], ['quests.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('quest_id', 'user_id')
    )

    op.create_table('group_members',
        sa.Column('group_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.Enum('member', 'moderator', 'admin', 'owner', name='grouprole')),
        sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean()),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('group_id', 'user_id')
    )

    # Create quest_progress table
    op.create_table('quest_progress',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('quest_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('checkpoint_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('verified_latitude', sa.Float(), nullable=True),
        sa.Column('verified_longitude', sa.Float(), nullable=True),
        sa.Column('verification_photo_url', sa.String(length=500), nullable=True),
        sa.Column('points_earned', sa.Integer(), nullable=False),
        sa.Column('progress_data', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['checkpoint_id'], ['quest_checkpoints.id'], ),
        sa.ForeignKeyConstraint(['quest_id'], ['quests.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_progress_completion', 'quest_progress', ['is_completed', 'completed_at'], unique=False)
    op.create_index('idx_progress_user_quest', 'quest_progress', ['user_id', 'quest_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('quest_progress')
    op.drop_table('group_members')
    op.drop_table('quest_participants')
    op.drop_table('quest_checkpoints')
    op.drop_table('user_stats')
    op.drop_table('user_rewards')
    op.drop_table('user_achievements')
    op.drop_table('quests')
    op.drop_table('groups')
    op.drop_table('friendships')
    op.drop_table('achievements')
    op.drop_table('locations')
    op.drop_table('users')
    op.drop_table('cities')
    
    # Drop enum types
    op.execute("DROP TYPE IF EXISTS friendshipstatus")
    op.execute("DROP TYPE IF EXISTS grouprole")
    op.execute("DROP TYPE IF EXISTS questdifficulty")
    op.execute("DROP TYPE IF EXISTS queststatus")