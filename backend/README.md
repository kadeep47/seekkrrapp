# Seeker Backend API

FastAPI-based backend for the Seeker location-based questing platform.

## Features

- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **SQLAlchemy ORM**: Database abstraction with Alembic migrations
- **Redis Integration**: Caching and session management
- **JWT Authentication**: Secure token-based authentication
- **Comprehensive Logging**: Structured logging with request tracking
- **Error Handling**: Consistent error responses and exception handling
- **OpenAPI Documentation**: Auto-generated API documentation
- **Testing Framework**: Pytest with coverage reporting
- **Docker Support**: Containerized development and deployment

## Project Structure

```
backend/
├── src/                    # Source code
│   ├── api/               # API routes and endpoints
│   ├── auth/              # Authentication service
│   ├── users/             # User management service
│   ├── quests/            # Quest management service
│   ├── rewards/           # Reward engine service
│   ├── social/            # Social features service
│   ├── common/            # Shared utilities and middleware
│   └── database/          # Database models and configuration
├── tests/                 # Test files
├── scripts/               # Utility scripts
├── alembic/               # Database migrations
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp ../.env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database**
   ```bash
   python scripts/init_db.py
   ```

5. **Run development server**
   ```bash
   python scripts/dev.py
   ```

### Using Docker

```bash
# From project root
docker-compose up -d
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_main.py -v
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Downgrade migration
alembic downgrade -1
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## Configuration

The application uses environment variables for configuration. Key settings:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT signing key
- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## API Endpoints

### Core Endpoints

- `GET /`: API information
- `GET /health`: Health check
- `GET /api/v1/status`: API status

### Authentication (Coming Soon)

- `POST /api/v1/auth/register`: User registration
- `POST /api/v1/auth/login`: User login
- `POST /api/v1/auth/refresh`: Token refresh
- `POST /api/v1/auth/logout`: User logout

### Users (Coming Soon)

- `GET /api/v1/users/profile`: Get user profile
- `PUT /api/v1/users/profile`: Update user profile
- `GET /api/v1/users/stats`: Get user statistics

### Quests (Coming Soon)

- `GET /api/v1/quests/cities`: List cities
- `GET /api/v1/quests`: List quests
- `POST /api/v1/quests/{id}/join`: Join quest
- `PUT /api/v1/quests/{id}/progress`: Update progress

## Error Handling

All API responses follow a consistent format:

### Success Response
```json
{
  "success": true,
  "data": {...},
  "message": "Optional message",
  "timestamp": "2024-01-01T00:00:00Z",
  "request_id": "uuid"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ErrorType",
    "message": "Human readable message",
    "details": {...}
  },
  "request_id": "uuid",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Logging

The application uses structured logging with the following levels:

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about application flow
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures

Logs include request IDs for tracing requests across the system.

## Security

- JWT-based authentication
- CORS configuration for cross-origin requests
- Request rate limiting (coming soon)
- Input validation and sanitization
- SQL injection prevention through ORM
- Secure password hashing with bcrypt

## Performance

- Connection pooling for database connections
- Redis caching for frequently accessed data
- Async/await for non-blocking operations
- Response compression
- Database query optimization

## Deployment

### Production Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up Redis cluster
- [ ] Configure HTTPS
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline

### Environment Variables

```bash
# Production settings
DATABASE_URL=postgresql://user:pass@host:5432/seeker_prod
REDIS_URL=redis://redis-host:6379
SECRET_KEY=your-super-secret-key
DEBUG=false
LOG_LEVEL=INFO
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.