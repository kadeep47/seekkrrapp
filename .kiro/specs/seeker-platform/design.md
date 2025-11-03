# Seeker Platform Design Document

## Overview

The Seeker platform implements a modern, scalable architecture that separates concerns between frontend clients (web and mobile) and backend services. This design follows industry best practices used by companies like Airbnb, Uber, and Meta for managing multi-platform applications with shared backend infrastructure.

### Architecture Philosophy

- **API-First Design**: All functionality exposed through well-defined REST/GraphQL APIs
- **Client Agnostic Backend**: Business logic independent of client implementation
- **Modular Frontend**: Separate but consistent implementations for web and mobile
- **Scalable Infrastructure**: Designed to grow from MVP to enterprise scale
- **Developer Experience**: Automated tooling for consistency and productivity

## Architecture

### High-Level System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │  Android App    │    │    iOS App      │
│  (React/TS)     │    │ (Kotlin/Compose)│    │ (Swift/SwiftUI) │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │      API Gateway          │
                    │   (Load Balancer +        │
                    │    Rate Limiting)         │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │    Backend Services       │
                    │   (FastAPI/NestJS)        │
                    │                           │
                    │  ┌─────┐ ┌─────┐ ┌─────┐ │
                    │  │Auth │ │Quest│ │User │ │
                    │  │ Svc │ │ Svc │ │ Svc │ │
                    │  └─────┘ └─────┘ └─────┘ │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │     Data Layer            │
                    │                           │
                    │ ┌─────────┐ ┌───────────┐ │
                    │ │PostgreSQL│ │   Redis   │ │
                    │ │(Primary) │ │  (Cache)  │ │
                    │ └─────────┘ └───────────┘ │
                    └───────────────────────────┘
```

### Recommended Folder Structure

Based on your requirements and industry best practices, here's the optimal structure:

```
seeker/
├── content/                    # Web application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Route-based page components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── services/          # API client services (generated)
│   │   ├── stores/            # Zustand state management
│   │   ├── types/             # TypeScript type definitions (generated)
│   │   └── utils/             # Utility functions
│   ├── public/                # Static assets
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── backend/                   # API server
│   ├── src/
│   │   ├── auth/              # Authentication service
│   │   ├── users/             # User management service
│   │   ├── quests/            # Quest management service
│   │   ├── rewards/           # Reward engine service
│   │   ├── social/            # Social features service
│   │   ├── common/            # Shared utilities and middleware
│   │   ├── database/          # Database models and migrations
│   │   └── api/               # API route definitions
│   ├── tests/                 # Backend tests
│   ├── docs/                  # API documentation
│   ├── requirements.txt       # Python dependencies
│   └── openapi.yaml          # API specification
│
├── apps/                      # Mobile applications
│   └── mobile/                # Flutter app (cross-platform)
│       ├── lib/
│       │   ├── main.dart      # App entry point
│       │   ├── core/          # Core utilities and constants
│       │   ├── features/      # Feature-based organization
│       │   │   ├── auth/      # Authentication feature
│       │   │   ├── quests/    # Quest management feature
│       │   │   ├── profile/   # User profile feature
│       │   │   └── social/    # Social features
│       │   ├── shared/        # Shared widgets and services
│       │   │   ├── widgets/   # Reusable UI components
│       │   │   ├── services/  # API services (generated)
│       │   │   ├── models/    # Data models (generated)
│       │   │   └── utils/     # Utility functions
│       │   └── theme/         # App theming and design tokens
│       ├── android/           # Android-specific configuration
│       ├── ios/               # iOS-specific configuration
│       ├── pubspec.yaml       # Flutter dependencies
│       └── analysis_options.yaml
│
├── packages/                  # Shared libraries (future)
│   ├── api-contract/          # OpenAPI specifications
│   ├── api-sdk/              # Generated client SDKs
│   └── design-tokens/        # Shared design system
│
├── tools/                    # Development tools
│   ├── codegen/              # Code generation scripts
│   └── scripts/              # Build and deployment scripts
│
├── docs/                     # Project documentation
├── docker-compose.yml        # Local development environment
├── package.json              # Root package.json for monorepo
└── README.md
```

## Components and Interfaces

### Backend Services Architecture

#### 1. Authentication Service (`/auth`)
- **Purpose**: Handle user registration, login, JWT token management
- **Key Components**:
  - User registration and validation
  - JWT token generation and refresh
  - OAuth integration (Google, Apple, Facebook)
  - Password reset functionality
- **Database Tables**: `users`, `user_sessions`, `oauth_providers`

#### 2. User Management Service (`/users`)
- **Purpose**: Manage user profiles, preferences, and settings
- **Key Components**:
  - Profile management (avatar, bio, preferences)
  - User statistics and achievements
  - Privacy settings
- **Database Tables**: `user_profiles`, `user_preferences`, `user_stats`

#### 3. Quest Management Service (`/quests`)
- **Purpose**: Core quest functionality and location-based features
- **Key Components**:
  - Quest creation and management
  - Location verification and tracking
  - Quest progress tracking
  - City and region management
- **Database Tables**: `quests`, `quest_participants`, `quest_progress`, `cities`, `locations`

#### 4. Reward Engine (`/rewards`)
- **Purpose**: Handle points, achievements, and reward distribution
- **Key Components**:
  - Point calculation and distribution
  - Achievement system
  - Leaderboards
  - Reward redemption
- **Database Tables**: `user_rewards`, `achievements`, `leaderboards`, `reward_transactions`

#### 5. Social System (`/social`)
- **Purpose**: Group management and social interactions
- **Key Components**:
  - Group creation and management
  - Friend systems
  - Activity feeds
  - Group quests and challenges
- **Database Tables**: `groups`, `group_members`, `friendships`, `activity_feeds`

### API Design Patterns

#### RESTful API Structure
```
/api/v1/
├── /auth
│   ├── POST /register
│   ├── POST /login
│   ├── POST /refresh
│   └── POST /logout
├── /users
│   ├── GET /profile
│   ├── PUT /profile
│   └── GET /stats
├── /quests
│   ├── GET /cities
│   ├── GET /cities/{cityId}/quests
│   ├── POST /quests/{questId}/join
│   └── PUT /quests/{questId}/progress
├── /rewards
│   ├── GET /achievements
│   ├── GET /leaderboard
│   └── POST /redeem
└── /social
    ├── GET /groups
    ├── POST /groups
    └── GET /feed
```

### Frontend Architecture

#### Web Application (React + TypeScript)
- **State Management**: Zustand for global state, React Query for server state
- **Styling**: Tailwind CSS with custom design tokens
- **Routing**: React Router v6 with lazy loading
- **API Integration**: Generated TypeScript SDK from OpenAPI spec
- **Build Tool**: Vite for fast development and optimized builds

#### Mobile Application (Flutter)

##### Flutter Cross-Platform App
- **Architecture**: Clean Architecture with BLoC pattern
- **State Management**: Flutter BLoC for complex state, Provider for simple state
- **Dependency Injection**: GetIt service locator
- **Networking**: Dio HTTP client with generated API interfaces
- **Local Storage**: Hive for lightweight storage, SQLite for complex data
- **Navigation**: GoRouter for declarative routing
- **UI Framework**: Material Design 3 with custom theming
- **Platform Integration**: Platform channels for native features (camera, location, notifications)

## Data Models

### Core Entity Relationships

```mermaid
erDiagram
    User ||--o{ UserProfile : has
    User ||--o{ QuestParticipant : participates
    User ||--o{ UserReward : earns
    User ||--o{ GroupMember : joins
    
    Quest ||--o{ QuestParticipant : includes
    Quest }o--|| City : located_in
    Quest ||--o{ QuestProgress : tracks
    
    Group ||--o{ GroupMember : contains
    Group ||--o{ GroupQuest : organizes
    
    City ||--o{ Quest : hosts
    City ||--o{ Location : contains
    
    User {
        uuid id PK
        string email UK
        string password_hash
        timestamp created_at
        timestamp updated_at
        boolean is_active
    }
    
    Quest {
        uuid id PK
        string title
        text description
        uuid city_id FK
        json location_data
        integer difficulty_level
        integer max_participants
        timestamp start_time
        timestamp end_time
        boolean is_active
    }
    
    City {
        uuid id PK
        string name
        string country
        decimal latitude
        decimal longitude
        json metadata
    }
```

### API Response Formats

#### Standard Response Wrapper
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  meta?: {
    pagination?: PaginationInfo;
    timestamp: string;
  };
}
```

#### Quest Data Model
```typescript
interface Quest {
  id: string;
  title: string;
  description: string;
  city: {
    id: string;
    name: string;
    country: string;
  };
  difficulty: 'easy' | 'medium' | 'hard';
  duration: number; // minutes
  maxParticipants: number;
  currentParticipants: number;
  rewards: {
    points: number;
    achievements: string[];
  };
  location: {
    latitude: number;
    longitude: number;
    radius: number; // meters
  };
  startTime: string; // ISO 8601
  endTime: string; // ISO 8601
  status: 'upcoming' | 'active' | 'completed' | 'cancelled';
}
```

## Error Handling

### Error Classification System

#### 1. Client Errors (4xx)
- **400 Bad Request**: Invalid input data or malformed requests
- **401 Unauthorized**: Authentication required or invalid credentials
- **403 Forbidden**: Insufficient permissions for requested action
- **404 Not Found**: Requested resource does not exist
- **409 Conflict**: Resource conflict (e.g., duplicate registration)
- **422 Unprocessable Entity**: Valid format but business logic errors

#### 2. Server Errors (5xx)
- **500 Internal Server Error**: Unexpected server-side errors
- **502 Bad Gateway**: Upstream service failures
- **503 Service Unavailable**: Temporary service outages
- **504 Gateway Timeout**: Request timeout from upstream services

### Error Response Format
```typescript
interface ErrorResponse {
  error: {
    code: string; // Machine-readable error code
    message: string; // Human-readable error message
    field?: string; // Specific field for validation errors
    details?: {
      [key: string]: any; // Additional error context
    };
  };
  requestId: string; // For debugging and support
  timestamp: string; // ISO 8601 timestamp
}
```

### Client-Side Error Handling Strategy

#### Web Application
- **Global Error Boundary**: Catch and display unexpected React errors
- **API Error Interceptor**: Centralized handling of HTTP errors
- **User-Friendly Messages**: Convert technical errors to user-friendly text
- **Retry Logic**: Automatic retry for transient failures
- **Offline Support**: Graceful degradation when network is unavailable

#### Mobile Applications
- **Network Error Handling**: Detect and handle connectivity issues
- **Validation Feedback**: Real-time form validation with clear error messages
- **Crash Reporting**: Integration with crash analytics (Crashlytics, Sentry)
- **Offline Queue**: Queue actions when offline, sync when online

## Testing Strategy

### Backend Testing

#### 1. Unit Tests
- **Coverage Target**: 80%+ code coverage
- **Framework**: pytest (Python) or Jest (Node.js)
- **Focus Areas**:
  - Business logic validation
  - Data model operations
  - Utility functions
  - Authentication and authorization

#### 2. Integration Tests
- **Database Integration**: Test with real database connections
- **API Endpoint Testing**: Full request/response cycle testing
- **External Service Mocking**: Mock third-party APIs (OAuth, payment processors)
- **Environment**: Dedicated test database and Redis instance

#### 3. End-to-End Tests
- **Framework**: Playwright or Cypress
- **Scenarios**: Critical user journeys (registration, quest participation, rewards)
- **Data Management**: Test data setup and teardown
- **Environment**: Staging environment with production-like data

### Frontend Testing

#### Web Application Testing
- **Unit Tests**: Component testing with React Testing Library
- **Integration Tests**: User interaction flows
- **Visual Regression**: Screenshot comparison testing
- **Performance Tests**: Core Web Vitals monitoring

#### Mobile Application Testing (Flutter)
- **Unit Tests**: Business logic and utility functions using flutter_test
- **Widget Tests**: UI component testing with testWidgets
- **Integration Tests**: Full app flow testing with integration_test package
- **Golden Tests**: Screenshot comparison testing for UI consistency
- **Device Testing**: Multiple screen sizes and platform versions using device farms

### Testing Infrastructure

#### Continuous Integration Pipeline
```yaml
# Example GitHub Actions workflow
name: CI/CD Pipeline
on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: test
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=src tests/
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  web-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
        working-directory: ./content
      - name: Run tests
        run: npm test
        working-directory: ./content
```

## Technology Stack Recommendations

### Backend Technology Choice

#### Option 1: FastAPI (Python) - Recommended
**Pros:**
- Excellent performance and async support
- Automatic OpenAPI generation
- Strong typing with Pydantic
- Great ecosystem for AI/ML integration (future features)
- Easy deployment and scaling

**Cons:**
- Smaller ecosystem compared to Node.js
- Less JavaScript/TypeScript code sharing

#### Option 2: NestJS (Node.js/TypeScript)
**Pros:**
- Full TypeScript stack consistency
- Excellent decorator-based architecture
- Strong enterprise patterns
- Great testing support

**Cons:**
- More complex setup
- Higher memory usage
- Less mature async ecosystem

### Database Architecture

#### Primary Database: PostgreSQL
- **Reasons**: ACID compliance, JSON support, excellent performance, mature ecosystem
- **Configuration**: 
  - Connection pooling with PgBouncer
  - Read replicas for scaling
  - Automated backups and point-in-time recovery

#### Caching Layer: Redis
- **Use Cases**: Session storage, API response caching, real-time features
- **Configuration**: Redis Cluster for high availability

#### Search Engine: Elasticsearch (Future)
- **Use Cases**: Quest search, user discovery, analytics
- **Integration**: When search requirements become complex

### Development Tools and Workflow

#### Code Generation Pipeline
```bash
# OpenAPI to TypeScript SDK generation
openapi-generator generate \
  -i backend/docs/openapi.yaml \
  -g typescript-fetch \
  -o content/src/services/generated

# OpenAPI to Dart SDK generation
openapi-generator generate \
  -i backend/docs/openapi.yaml \
  -g dart \
  -o apps/mobile/lib/shared/services/generated
```

#### Monorepo Management

##### When to Introduce Monorepo Tools

**Phase 1 (MVP)**: Simple folder structure, manual coordination
- **Timeline**: 0-6 months
- **Team Size**: 1-3 developers
- **Complexity**: Low, manageable with npm workspaces

**Phase 2 (Growth)**: Introduce Turborepo or Nx
- **Timeline**: 6-18 months
- **Team Size**: 4-10 developers
- **Triggers**: 
  - Shared code between projects
  - Complex build dependencies
  - Need for coordinated deployments

**Phase 3 (Scale)**: Advanced monorepo with custom tooling
- **Timeline**: 18+ months
- **Team Size**: 10+ developers
- **Features**: Custom build systems, advanced caching, micro-frontends

##### Recommended Monorepo Tool: Turborepo
```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", "build/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": []
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false
    }
  }
}
```

## Industry Best Practices Analysis

### How Top Companies Handle Multi-Platform Architecture

#### Airbnb's Approach
- **Backend**: Service-oriented architecture with Ruby on Rails and Java
- **Web**: React with server-side rendering
- **Mobile**: Native apps with shared design system
- **Key Insight**: Heavy investment in design systems and component libraries

#### Uber's Architecture
- **Backend**: Microservices with Go and Java
- **Web**: React with micro-frontend architecture
- **Mobile**: Native apps with shared business logic through libraries
- **Key Insight**: Domain-driven service boundaries, extensive A/B testing infrastructure

#### Meta's Strategy
- **Backend**: Hack/PHP with extensive caching layers
- **Web**: React (they created it)
- **Mobile**: React Native for cross-platform development
- **Key Insight**: Significant investment in developer tooling and build systems

### Recommended Evolution Path

#### Phase 1: MVP (Months 1-6)
- **Goal**: Validate product-market fit
- **Architecture**: Monolithic backend, React web app, Flutter mobile app
- **Team**: 1-3 full-stack developers
- **Focus**: Core features, cross-platform mobile app with Flutter
- **Mobile Strategy**: Single Flutter codebase for both iOS and Android

#### Phase 2: Growth (Months 6-18)
- **Goal**: Scale user base and features
- **Architecture**: Modular monolith, optimized frontends
- **Team**: 4-8 developers (backend, web, Flutter specialists)
- **Focus**: Performance optimization, advanced features, platform-specific optimizations
- **Mobile Strategy**: Optimize Flutter app, consider platform channels for native features

#### Phase 3: Scale (Months 18+)
- **Goal**: Enterprise-grade platform
- **Architecture**: Microservices, advanced tooling
- **Team**: 10+ developers across multiple teams
- **Focus**: Global scaling, advanced analytics, AI features
- **Mobile Strategy**: Evaluate native apps if Flutter limitations become significant, or continue with optimized Flutter

## Deployment and Infrastructure

### Development Environment
```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: seeker_dev
      POSTGRES_USER: seeker
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://seeker:dev_password@postgres:5432/seeker_dev
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app

  web:
    build: ./content
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://localhost:8000
    volumes:
      - ./content:/app

volumes:
  postgres_data:
```

### Production Deployment Strategy

#### Cloud Provider: AWS (Recommended)
- **Compute**: ECS Fargate for containerized services
- **Database**: RDS PostgreSQL with Multi-AZ deployment
- **Caching**: ElastiCache Redis
- **Storage**: S3 for file uploads and static assets
- **CDN**: CloudFront for global content delivery
- **Load Balancing**: Application Load Balancer

#### Alternative: Google Cloud Platform
- **Compute**: Cloud Run for serverless containers
- **Database**: Cloud SQL PostgreSQL
- **Caching**: Memorystore Redis
- **Storage**: Cloud Storage
- **CDN**: Cloud CDN

### CI/CD Pipeline Architecture

```mermaid
graph LR
    A[Developer Push] --> B[GitHub Actions]
    B --> C[Run Tests]
    C --> D[Build Images]
    D --> E[Deploy to Staging]
    E --> F[Integration Tests]
    F --> G[Deploy to Production]
    
    C --> H[Generate SDKs]
    H --> I[Update Client Apps]
```

This design provides a comprehensive foundation for your Seeker platform that can scale from MVP to enterprise-level system while maintaining clean architecture principles and industry best practices.