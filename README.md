# IAM Service - Identity and Access Management

A comprehensive Identity and Access Management (IAM) service built with FastAPI, providing authentication, authorization, and user management capabilities.

## Features

- **Authentication**: JWT-based authentication with access and refresh tokens
- **Authorization**: Role-based access control (RBAC)
- **User Management**: Complete CRUD operations for user accounts
- **Security**: Password hashing, rate limiting, and security middleware
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Testing**: Comprehensive test suite
- **Docker Support**: Containerized deployment with Docker Compose

## Architecture

```
iam_service/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Core functionality (config, security, rate limiting)
│   ├── db/              # Database models and schemas
│   ├── models/          # SQLAlchemy models
│   ├── services/        # Business logic layer
│   └── utils/           # Utilities (logging, exception handling)
├── tests/               # Test suite
├── docs/                # Documentation
└── docker-compose.yaml  # Docker configuration
```

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd iam_service
```

2. Start the services:
```bash
docker-compose up -d
```

3. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite:///./iam_service.db"
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/logout-all` - Logout from all sessions

### User Management
- `POST /api/v1/users` - Create user (Admin only)
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `GET /api/v1/users` - List users (Admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID (Admin only)
- `PUT /api/v1/users/{user_id}` - Update user (Admin only)
- `DELETE /api/v1/users/{user_id}` - Delete user (Admin only)
- `PATCH /api/v1/users/{user_id}/status` - Change user status (Admin only)

## Configuration

Configure the application using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT secret key | `your-secret-key-change-in-production` |
| `DATABASE_URL` | Database connection URL | `sqlite:///./iam_service.db` |
| `DEBUG` | Debug mode | `False` |
| `HOST` | Application host | `0.0.0.0` |
| `PORT` | Application port | `8000` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiration | `7` |

## User Roles

- **Admin**: Full access to all endpoints and user management
- **Moderator**: Limited administrative capabilities
- **User**: Basic user account with self-management capabilities

## Security Features

- Password hashing using bcrypt
- JWT tokens with configurable expiration
- Rate limiting to prevent abuse
- CORS protection
- Input validation and sanitization
- Comprehensive error handling
- Structured logging

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/ -v
```

## Development

### Adding New Features

1. Create models in `app/models/`
2. Define schemas in `app/db/schemas.py`
3. Implement business logic in `app/services/`
4. Create API endpoints in `app/api/v1/`
5. Add tests in `tests/`

### Database Migrations

For production deployments, consider using Alembic for database migrations:

```bash
# Initialize migrations
alembic init migrations

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Deployment

### Docker Production Deployment

1. Build the production image:
```bash
docker build -t iam-service:latest .
```

2. Deploy with Docker Compose:
```bash
docker-compose -f docker-compose.prod.yaml up -d
```

### Environment Setup

For production, ensure you:
- Change the default `SECRET_KEY`
- Use a production database (PostgreSQL recommended)
- Enable HTTPS
- Configure proper CORS origins
- Set up monitoring and logging
- Implement backup strategies

## Monitoring

The service includes:
- Health check endpoint: `/health`
- Structured logging to files and console
- Request/response logging
- Error tracking and reporting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
