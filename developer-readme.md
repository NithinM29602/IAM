# IAM Service Developer Guide

This document serves as a comprehensive developer guide for the Identity and Access Management (IAM) service, explaining the project structure, architectural decisions, and implementation guidelines for each component.

## Architectural Philosophy

The IAM service follows a modular, domain-driven design architecture to achieve:

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Maintainability**: Code is organized to make it easier to understand, debug, and extend
3. **Testability**: Components are designed to be testable in isolation
4. **Scalability**: Service layers can be scaled independently as needed

## Project Structure Overview

The IAM service architecture is organized into logical modules, each with specific responsibilities:

### `/app` - Core Application

The main application code lives here, organized into several subdirectories following a layered architecture pattern:

#### `/app/main.py`
**Purpose**: Application entry point that bootstraps the entire service.
**Implementation Details**:
- Configures FastAPI application settings
- Sets up middleware (CORS, request logging)
- Registers API routers 
- Manages application lifecycle events (startup/shutdown)
- Connects and disconnects from MongoDB

**When to modify**: When adding new API routes, middleware, or changing application-wide behaviors.

#### `/app/api` - API Layer
**Purpose**: Contains all HTTP request handlers, organized by API version and domain.
**Implementation Guidelines**:
- Keep route handlers thin - they should only:
  - Validate inputs using Pydantic models
  - Call appropriate services
  - Transform service responses to HTTP responses
  - Handle HTTP-specific concerns (status codes, headers)
- No business logic should be present here

**API Versioning**:
- `/app/api/v1/auth.py`: Authentication endpoints (sign-up, sign-in, token refresh)
  - These endpoints manage user registration and authentication flows
  - Authentication endpoints should never perform data manipulation beyond what's needed for auth
  
- `/app/api/v1/users.py`: User management endpoints (CRUD operations)
  - These endpoints handle user profile management
  - Always protect these endpoints with proper authorization

**When to add new routes**:
- When exposing new business capabilities via API
- When creating new resource types in your system

#### `/app/core` - Core Framework Components
**Purpose**: Contains application-wide utilities and configurations.

- `/app/core/config.py`: 
  **Purpose**: Centralized configuration management
  **Implementation**: Uses Pydantic Settings classes to:
    - Load and validate environment variables
    - Provide typed configuration access throughout the app
    - Set sensible defaults
  **When to modify**: When adding new configuration options or environment variables
  
- `/app/core/security.py`: 
  **Purpose**: Security primitives and utilities
  **Implementation**:
    - Password hashing and verification (using bcrypt)
    - JWT token generation and validation
    - Permission verification logic
  **When to modify**: When changing authentication methods or security requirements
  
- `/app/core/rate_limit.py`: 
  **Purpose**: Protect API from abuse
  **Implementation**:
    - Request rate limiting based on IP or user ID
    - Backoff strategies for repeated requests
  **When to modify**: When adjusting rate limits or changing rate limiting strategy

#### `/app/db` - Database Layer
**Purpose**: Database connection management and low-level data access.

- `/app/db/database.py`: 
  **Purpose**: MongoDB connection management
  **Implementation**:
    - Async connection handling with Motor
    - Connection pooling
    - Database lifecycle management
  **When to modify**: When changing database providers or connection parameters
  
- `/app/db/schemas.py`: 
  **Purpose**: Database schema definitions
  **Implementation**:
    - MongoDB collection indexes
    - Database-specific validation rules
  **When to modify**: When adding new collections or modifying existing database schemas

#### `/app/dependencies` - FastAPI Dependencies
**Purpose**: Contains reusable FastAPI dependencies for request processing.

- `/app/dependencies/db.py`: 
  **Purpose**: Provides database access to route handlers
  **Implementation**:
    - Async dependency functions that yield database collections
    - Error handling for database connection issues
  **When to modify**: When adding new collections or changing database access patterns
  **Usage**: Import and use in FastAPI route decorators for dependency injection

#### `/app/models` - Data Models
**Purpose**: Pydantic models for data validation, serialization, and documentation.

- `/app/models/user.py`: 
  **Purpose**: User-related data structures
  **Implementation**:
    - `UserBase` - Common user fields
    - `UserCreate` - Fields required for user creation with validation
    - `UserInDB` - How users are stored in the database
    - `User` - How users are presented in the API
  **When to modify**: When changing user data structure or validation rules
  
- `/app/models/token.py`: 
  **Purpose**: Authentication token representations
  **Implementation**:
    - `Token` - Token response structure
    - `TokenPayload` - JWT payload structure
    - `TokenData` - Token extraction structure
  **When to modify**: When changing token format or authentication flow

#### `/app/services` - Business Logic Layer
**Purpose**: Contains all business logic, isolated from HTTP and database concerns.

- `/app/services/auth_service.py`: 
  **Purpose**: Authentication business logic
  **Implementation**:
    - User credential validation
    - Token generation and validation
    - Authentication workflows
  **When to modify**: When changing authentication processes or security requirements
  
- `/app/services/user_service.py`: 
  **Purpose**: User management business logic
  **Implementation**:
    - User creation, retrieval, update, and deletion
    - User profile management
    - User permission checks
  **When to modify**: When changing user-related business rules or adding new user capabilities

**Service Layer Guidelines**:
- Services should be stateless and dependency-injected
- Business logic should be independent of HTTP and database details
- Services should throw domain-specific exceptions, not HTTP exceptions
- Services should return domain models, not database models or HTTP responses

#### `/app/utils` - Utility Functions
**Purpose**: Cross-cutting utilities used throughout the application.

- `/app/utils/logger.py`: 
  **Purpose**: Centralized logging configuration
  **Implementation**:
    - Configurable log levels
    - Structured logging
    - Log rotation settings
  **When to modify**: When changing logging behavior or adding logging destinations
  
- `/app/utils/exception_handler.py`: 
  **Purpose**: Global exception handling
  **Implementation**:
    - Maps exceptions to appropriate HTTP responses
    - Formats error messages consistently
    - Handles validation errors gracefully
  **When to modify**: When adding new exception types or changing error response formats

### `/docs` - Documentation

**Purpose**: Contains project documentation for both developers and API consumers.

- `/docs/api`: 
  **Purpose**: API documentation
  **Contents**:
    - OpenAPI specifications automatically generated from FastAPI
    - API reference guides
    - Example requests and responses
  **When to update**: When changing API endpoints, parameters, or response structures

- `/docs/architecture`: 
  **Purpose**: Architecture and design documentation
  **Contents**:
    - System architecture diagrams
    - Component interaction specifications
    - Design decisions and rationales
  **When to update**: When making significant architectural changes or design decisions

### `/tests` - Test Suite

**Purpose**: Contains automated tests to ensure code quality and correctness.

- `/tests/test_auth.py`: 
  **Purpose**: Authentication-related tests
  **Test types**:
    - Unit tests for authentication services
    - Integration tests for authentication flows
    - Endpoint tests for auth API routes
  **When to update**: When modifying authentication logic or adding new auth features

- `/tests/test_users.py`: 
  **Purpose**: User management tests
  **Test types**:
    - Unit tests for user services
    - Integration tests for user operations
    - Endpoint tests for user API routes
  **When to update**: When modifying user-related logic or adding new user features

**Testing Guidelines**:
- Always maintain >80% test coverage
- Use pytest fixtures for test setup and teardown
- Mock external dependencies in unit tests
- Use MongoDB test containers for integration tests

## Key Components Usage Guide

### Authentication Flow Implementation

Our authentication system implements OAuth 2.0 password flow with JWT tokens. Here's how it works:

1. **User Registration** (`/app/api/v1/auth.py` `sign_up` endpoint):
   - Receives email and password from client
   - Validates input format using Pydantic models
   - Checks if user already exists
   - Hashes password securely using bcrypt in `security.py`
   - Stores user record in MongoDB
   - Returns user information (excluding password)

   ```python
   # Example implementation
   @router.post("/signup", response_model=User)
   async def sign_up(
       user_create: UserCreate, 
       user_collections: AsyncIOMotorCollection = Depends(get_user_collections)
   ):
       existing_user = await get_user_by_email(user_create.email, user_collections)
       if existing_user:
           raise HTTPException(status_code=400, detail="Email already registered")
       return await create_user(user_create, user_collections)
   ```

2. **User Authentication** (`/app/api/v1/auth.py` `sign_in` endpoint):
   - Receives email and password from client
   - Verifies credentials against database
   - Generates JWT token with appropriate claims and expiration
   - Returns token to client

   ```python
   # Example implementation
   @router.post("/signin", response_model=Token)
   async def sign_in(
       credentials: LoginCredentials,
       user_collections: AsyncIOMotorCollection = Depends(get_user_collections)
   ):
       user = await authenticate_user(credentials.email, credentials.password, user_collections)
       if not user:
           raise HTTPException(status_code=401, detail="Invalid credentials")
       
       # Create access token with 30 minutes expiration
       access_token = create_access_token(
           data={"sub": str(user.id), "admin": user.is_admin},
           expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
       )
       return {"access_token": access_token, "token_type": "bearer"}
   ```

3. **Token Validation** (implemented in `/app/core/security.py`):
   - Extracts JWT from request header
   - Verifies token signature and expiration
   - Decodes token payload
   - Injects user information into request context

   ```python
   # Example token validation dependency
   async def get_current_user(
       token: str = Depends(oauth2_scheme),
       user_collections: AsyncIOMotorCollection = Depends(get_user_collections)
   ) -> UserInDB:
       credentials_exception = HTTPException(
           status_code=401,
           detail="Invalid authentication credentials",
           headers={"WWW-Authenticate": "Bearer"},
       )
       try:
           payload = jwt.decode(
               token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
           )
           user_id: str = payload.get("sub")
           if user_id is None:
               raise credentials_exception
           token_data = TokenData(user_id=user_id)
       except JWTError:
           raise credentials_exception
           
       user = await get_user_by_id(token_data.user_id, user_collections)
       if user is None:
           raise credentials_exception
       return user
   ```

### Adding New API Endpoints

When adding new functionality to the API, follow these detailed steps:

1. **Define Models** in `/app/models/`:
   - Create request and response models using Pydantic
   - Implement validation rules specific to your business requirements
   - Use inheritance to create request/response variations

   ```python
   # Example model definition
   class ResourceBase(BaseModel):
       name: str
       description: str = None
       
   class ResourceCreate(ResourceBase):
       owner_id: str = None
       
       @field_validator('name')
       @classmethod
       def name_must_not_be_empty(cls, v):
           if not v or not v.strip():
               raise ValueError('Name cannot be empty')
           return v.strip()
           
   class ResourceInDB(ResourceBase):
       id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
       owner_id: str
       created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
       updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
       
       class Config:
           arbitrary_types_allowed = True
           populate_by_name = True
           json_schema_extra = {"example": {...}}
   ```

2. **Implement Service Logic** in `/app/services/`:
   - Create a new service file for your resource (e.g., `resource_service.py`)
   - Implement CRUD operations and business logic
   - Handle database interactions through the service
   - Keep services focused on business logic, not HTTP concerns

   ```python
   # Example service implementation
   async def create_resource(
       resource: ResourceCreate, 
       user_id: str,
       collection: AsyncIOMotorCollection
   ) -> ResourceInDB:
       resource_dict = resource.dict()
       resource_dict["owner_id"] = user_id
       resource_dict["created_at"] = datetime.now(timezone.utc)
       resource_dict["updated_at"] = datetime.now(timezone.utc)
       
       result = await collection.insert_one(resource_dict)
       created_resource = await collection.find_one({"_id": result.inserted_id})
       return ResourceInDB.parse_obj(created_resource)
   ```

3. **Create Router** in `/app/api/v1/`:
   - Add a new file for your resource routes (e.g., `resources.py`)
   - Define appropriate HTTP methods (GET, POST, PUT, DELETE)
   - Use dependencies for authentication and database access
   - Implement proper error handling

   ```python
   # Example router implementation
   from fastapi import APIRouter, Depends, HTTPException
   from app.dependencies.db import get_resource_collection
   from app.core.security import get_current_user
   
   router = APIRouter(prefix="/resources", tags=["resources"])
   
   @router.post("/", response_model=Resource)
   async def create_resource(
       resource: ResourceCreate,
       current_user: UserInDB = Depends(get_current_user),
       collection: AsyncIOMotorCollection = Depends(get_resource_collection)
   ):
       return await create_resource(resource, current_user.id, collection)
   ```

4. **Register Router** in `/app/main.py`:
   - Import your new router
   - Include it in the FastAPI application with the appropriate prefix

   ```python
   # In main.py
   from app.api.v1 import auth, users, resources
   
   # When setting up the application
   app.include_router(resources.router, prefix=settings.API_V1_STR)
   ```

5. **Update Documentation**:
   - Add appropriate OpenAPI tags and descriptions
   - Document expected responses and errors
   - Update architecture documentation if needed

### Database Operations Best Practices

MongoDB is used as the primary database, accessed through Motor for async operations:

1. **Connection Management**:
   - Database connection is managed in `/app/db/database.py`
   - Connection pooling is configured to optimize performance
   - Use connection events for logging and monitoring
   - Connection parameters are set via environment variables

   ```python
   # Example configuration
   client = AsyncIOMotorClient(
       settings.MONGODB_URL,
       maxPoolSize=settings.MONGO_MAX_POOL_SIZE,
       minPoolSize=settings.MONGO_MIN_POOL_SIZE,
       serverSelectionTimeoutMS=settings.MONGO_SERVER_TIMEOUT_MS
   )
   ```

2. **Collection Access**:
   - Use `/app/dependencies/db.py` to access collections in endpoints
   - Each resource type should have a dedicated dependency function
   - Add proper error handling and logging

   ```python
   # Example collection dependency
   async def get_resource_collection() -> AsyncIOMotorCollection:
       """Returns the resource collection from MongoDB."""
       logger.info("Fetching resource collection...")
       try:
           if not mongodb.db:
               await mongodb.connect()
           return mongodb.db[settings.MONGO_COLLECTION_RESOURCES]
       except Exception as e:
           logger.error(f"Failed to get resource collection: {e}")
           raise HTTPException(
               status_code=500, 
               detail="Database connection error"
           )
   ```


3. **Query Patterns**:
   - Use projection to limit returned fields
   - Implement pagination for large result sets
   - Use aggregation pipeline for complex queries
   - Handle MongoDB-specific error codes

   ```python
   # Example query with projection and pagination
   async def list_resources(
       skip: int = 0, 
       limit: int = 100,
       owner_id: str = None,
       collection: AsyncIOMotorCollection
   ) -> List[ResourceInDB]:
       query = {"owner_id": owner_id} if owner_id else {}
       cursor = collection.find(
           query,
           projection={"name": 1, "description": 1, "owner_id": 1, "created_at": 1}
       ).skip(skip).limit(limit).sort("created_at", -1)
       
       resources = []
       async for doc in cursor:
           resources.append(ResourceInDB.parse_obj(doc))
       return resources
   ```

### Error Handling Strategy

Proper error handling is crucial for API stability and developer experience:

1. **Global Exception Handlers**:
   - Custom exception handling in `/app/utils/exception_handler.py`
   - Consistent error response format
   - Detailed validation error messages
   - Privacy-aware error exposure

   ```python
   # Example exception handler
   @app.exception_handler(RequestValidationError)
   async def validation_exception_handler(request: Request, exc: RequestValidationError):
       """Handles validation errors and returns a structured JSON response."""
       errors = []
       for error in exc.errors():
           error_loc = " -> ".join(str(loc) for loc in error["loc"] if loc != "body")
           errors.append({
               "field": error_loc,
               "message": error["msg"],
               "type": error["type"]
           })
           
       return JSONResponse(
           status_code=422,
           content={
               "detail": "Validation error",
               "errors": errors
           },
       )
   ```

2. **Domain-Specific Exceptions**:
   - Create custom exception classes for business logic errors
   - Map domain exceptions to appropriate HTTP status codes
   - Include relevant context in error messages
   - Log detailed error information

   ```python
   # Example custom exception
   class ResourceNotFoundError(Exception):
       def __init__(self, resource_id: str):
           self.resource_id = resource_id
           self.message = f"Resource with ID {resource_id} not found"
           super().__init__(self.message)
   
   # Exception handler registration
   @app.exception_handler(ResourceNotFoundError)
   async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError):
       return JSONResponse(
           status_code=404,
           content={"detail": exc.message},
       )
   ```

### Logging Best Practices

Proper logging is essential for monitoring, debugging, and auditing:

1. **Logger Configuration**:
   - Use the logger from `/app/utils/logger.py` for consistent logging
   - Configure log levels via environment variables
   - Implement structured logging for easier parsing
   - Configure log rotation to prevent disk space issues

   ```python
   # Example logger usage
   from app.utils.logger import get_logger
   logger = get_logger(__name__)
   
   logger.debug("Detailed debug information")
   logger.info("User %s logged in successfully", user_id)
   logger.warning("Rate limit reached for user %s", user_id)
   logger.error("Failed to process request: %s", str(error))
   logger.critical("Database connection lost", extra={"connection_id": conn_id})
   ```

2. **What to Log**:
   - **Authentication events**: Sign-in attempts, sign-outs, token refreshes
   - **Resource operations**: Creation, updates, deletions
   - **Performance metrics**: Response times, database query durations
   - **Security events**: Permission denials, rate limit violations
   - **Application lifecycle**: Startup, shutdown, configuration changes

3. **Privacy and Security**:
   - Never log sensitive information (passwords, tokens, PII)
   - Mask or hash sensitive fields before logging
   - Consider GDPR and other privacy regulations
   - Implement proper log access controls

## Development Workflow

### Local Development Setup

1. **Environment Setup**:
   - Create a Python virtual environment:
     ```bash
     python -m venv iam_env
     source iam_env/bin/activate  # On Windows: iam_env\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Create a `.env` file with local configuration:
     ```
     SECRET_KEY=your_local_dev_secret_key
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE=30
     MONGODB_URL=mongodb://localhost:27017/
     MONGODB_DB=iam_dev
     MONGO_COLLECTION_USERINFO=userInfo
     LOG_LEVEL=DEBUG
     LOG_DIR=./logs
     ```

2. **Database Setup**:
   - Start MongoDB locally using Docker:
     ```bash
     docker-compose up -d mongodb
     ```
   - Monitor MongoDB logs if needed:
     ```bash
     docker-compose logs -f mongodb
     ```

3. **Running the Application**:
   - Start the application in development mode:
     ```bash
     uvicorn app.main:app --reload --port 8081
     ```
   - Access the API documentation at http://localhost:8081/iam/v1/docs
   - Monitor application logs in the `./logs` directory

4. **Development Cycle**:
   - Implement feature or fix
   - Write tests in `/tests` directory
   - Run tests:
     ```bash
     pytest -xvs tests/
     ```
   - Run linting:
     ```bash
     flake8 app/ tests/
     ```
   - Commit changes with descriptive commit messages

### API Development Guidelines

1. **Endpoint Design Principles**:
   - Use RESTful conventions for resource operations
   - Implement proper HTTP methods (GET, POST, PUT, DELETE)
   - Use consistent URL patterns:
     - Collection: `/iam/v1/users`
     - Resource: `/iam/v1/users/{user_id}`
     - Nested resources: `/iam/v1/users/{user_id}/permissions`

2. **Response Formats**:
   - Use consistent JSON structure
   - Include appropriate HTTP status codes
   - Provide helpful error messages
   - Document all responses in OpenAPI specification

3. **Request Validation**:
   - Use Pydantic models for input validation
   - Provide descriptive validation error messages
   - Validate at the model level, not in route handlers

4. **Performance Considerations**:
   - Use async handlers for I/O-bound operations
   - Implement database indexing for frequent queries
   - Use projection to limit returned fields
   - Implement pagination for large datasets

## Contribution Workflow

### Git Workflow

Follow this workflow when contributing new features or bug fixes to the IAM service:

1. **Sync with Main Branch**:
   - Always start by pulling the latest changes from the main branch:
     ```bash
     git checkout main
     git pull origin main
     ```

2. **Create Feature Branch**:
   - Create a new branch with a descriptive name using the format `your_name/short_name_task`:
     ```bash
     git checkout -b john_doe/user_permissions
     ```
   - Branch naming conventions:
     - Use your name as the prefix
     - Use a short, descriptive name for the feature or fix
     - Use underscores to separate words

3. **Implement Changes**:
   - Make your changes following the coding guidelines
   - Commit regularly with meaningful commit messages:
     ```bash
     git add .
     git commit -m "Add user permissions validation"
     ```
   - Keep commits focused and atomic

4. **Stay in Sync with Main**:
   - Periodically fetch and rebase from the main branch:
     ```bash
     git fetch origin
     git rebase origin/main
     ```
   - Resolve any conflicts that arise during rebasing:
     ```bash
     # After resolving conflicts
     git add .
     git rebase --continue
     ```

5. **Push Changes**:
   - Push your branch to the remote repository:
     ```bash
     git push origin your_name/short_name_task
     ```
   - For the first push, you may need to set the upstream:
     ```bash
     git push -u origin your_name/short_name_task
     ```

6. **Create Pull Request**:
   - Go to the repository on GitHub
   - Create a new pull request from your branch to main
   - Use a descriptive title and provide detailed information in the description
   - Reference any related issues using keywords (e.g., "Fixes #123")
   - Assign appropriate reviewers
   - Add relevant labels

7. **Code Review Process**:
   - Address reviewer comments promptly
   - Make requested changes as additional commits
   - Use "Request review" when ready for re-review
   - Once approved, prepare for merge

8. **Merge Strategy**:
   - Squash and merge for cleaner commit history
   - Use a descriptive commit message that summarizes all changes
   - Delete the branch after successful merge

### Code Quality Standards

1. **Testing Requirements**:
   - Write unit tests for all new functionality
   - Ensure tests pass locally before submitting PR
   - Maintain or improve code coverage

2. **Code Style**:
   - Follow PEP 8 guidelines for Python code
   - Use consistent naming conventions
   - Document public functions with docstrings
   - Run linters before committing

### PR Review Checklist

Before submitting a PR for review, ensure you've completed this checklist:

- [ ] Code follows project style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] Changes are rebased on latest main branch
- [ ] No debugging code or print statements left
- [ ] Sensitive information is not exposed
- [ ] Branch naming follows the convention

