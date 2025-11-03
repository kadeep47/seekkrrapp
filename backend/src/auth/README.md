# Authentication System

Comprehensive JWT-based authentication system for the Seeker platform.

## Features

- **User Registration**: Email-based registration with password validation
- **User Login**: Email/password authentication with JWT tokens
- **JWT Tokens**: Access and refresh token system
- **Password Security**: Bcrypt password hashing
- **Email Verification**: Email verification workflow
- **Password Reset**: Secure password reset via email
- **Token Refresh**: Automatic token refresh mechanism
- **User Management**: Account activation/deactivation
- **Security**: Comprehensive security measures and validation

## API Endpoints

### Authentication Endpoints

#### POST `/api/v1/auth/register`
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "username": "username",
      "first_name": "John",
      "last_name": "Doe",
      "is_verified": false,
      "created_at": "2024-01-01T00:00:00Z"
    },
    "tokens": {
      "access_token": "jwt_token",
      "refresh_token": "jwt_refresh_token",
      "token_type": "bearer",
      "expires_in": 1800
    }
  }
}
```

#### POST `/api/v1/auth/login`
Login with email and password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "username": "username",
      "last_login_at": "2024-01-01T00:00:00Z"
    },
    "tokens": {
      "access_token": "jwt_token",
      "refresh_token": "jwt_refresh_token",
      "token_type": "bearer",
      "expires_in": 1800
    }
  }
}
```

#### POST `/api/v1/auth/refresh`
Refresh access token using refresh token.

**Query Parameters:**
- `refresh_token`: The refresh token

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "new_jwt_token",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

#### GET `/api/v1/auth/me`
Get current user information (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "display_name": "John Doe",
    "bio": "User bio",
    "avatar_url": "https://example.com/avatar.jpg",
    "is_active": true,
    "is_verified": true,
    "profile_visibility": "public",
    "location_sharing": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

#### POST `/api/v1/auth/logout`
Logout user (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

#### POST `/api/v1/auth/forgot-password`
Send password reset email.

**Query Parameters:**
- `email`: User's email address

#### POST `/api/v1/auth/reset-password`
Reset password using reset token.

**Query Parameters:**
- `token`: Password reset token
- `new_password`: New password

#### POST `/api/v1/auth/change-password`
Change user password (requires authentication).

**Query Parameters:**
- `current_password`: Current password
- `new_password`: New password

#### POST `/api/v1/auth/verify-email/{user_id}`
Verify user email address.

#### GET `/api/v1/auth/validate-token`
Validate current token (requires authentication).

## Security Features

### Password Security
- **Bcrypt Hashing**: Passwords are hashed using bcrypt with salt
- **Minimum Length**: 8 character minimum password requirement
- **Secure Storage**: Passwords are never stored in plain text

### JWT Token Security
- **Access Tokens**: Short-lived (30 minutes) for API access
- **Refresh Tokens**: Long-lived (7 days) for token renewal
- **Token Types**: Separate token types prevent misuse
- **Expiration**: All tokens have expiration times
- **Signature**: Tokens are signed with secret key

### API Security
- **Authentication Required**: Protected endpoints require valid tokens
- **User Verification**: Some endpoints require email verification
- **Rate Limiting**: Protection against brute force attacks (future)
- **CORS**: Proper CORS configuration
- **Input Validation**: All inputs are validated

## Dependencies

The authentication system uses several dependencies:

### Core Dependencies
- **FastAPI**: Web framework
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation
- **python-jose**: JWT token handling
- **passlib**: Password hashing
- **bcrypt**: Password hashing algorithm

### Optional Dependencies
- **SMTP Server**: For email functionality
- **Redis**: For session management (future)

## Configuration

Authentication settings are configured via environment variables:

```bash
# JWT Configuration
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Usage Examples

### Client-Side Token Management

```javascript
// Store tokens after login
const loginResponse = await fetch('/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});

const { tokens } = await loginResponse.json();
localStorage.setItem('access_token', tokens.access_token);
localStorage.setItem('refresh_token', tokens.refresh_token);

// Use token for authenticated requests
const response = await fetch('/api/v1/auth/me', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});

// Refresh token when needed
const refreshResponse = await fetch(`/api/v1/auth/refresh?refresh_token=${refresh_token}`, {
  method: 'POST'
});
```

### Python Client Example

```python
import requests

# Login
login_data = {
    "email": "user@example.com",
    "password": "password123"
}

response = requests.post("http://localhost:8000/api/v1/auth/login", json=login_data)
tokens = response.json()["data"]["tokens"]

# Use token for authenticated requests
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
user_response = requests.get("http://localhost:8000/api/v1/auth/me", headers=headers)
```

## Error Handling

The authentication system provides detailed error responses:

### Common Error Codes
- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Authentication required or invalid credentials
- **403 Forbidden**: Insufficient permissions
- **409 Conflict**: Resource conflict (e.g., email already exists)
- **422 Unprocessable Entity**: Validation errors

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "AuthenticationError",
    "message": "Invalid email or password",
    "details": {}
  },
  "request_id": "uuid",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Testing

The authentication system includes comprehensive tests:

```bash
# Run authentication tests
pytest tests/test_auth.py -v

# Run with coverage
pytest tests/test_auth.py --cov=src.auth
```

## Future Enhancements

- **OAuth Integration**: Google, Apple, Facebook login
- **Two-Factor Authentication**: SMS/TOTP 2FA
- **Session Management**: Redis-based session storage
- **Rate Limiting**: Advanced rate limiting and abuse prevention
- **Audit Logging**: Comprehensive authentication audit logs
- **Device Management**: Track and manage user devices
- **Advanced Security**: Suspicious activity detection