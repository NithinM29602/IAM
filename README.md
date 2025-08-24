# IAM Service

This document provides instructions for setting up, running, and using the IAM (Identity and Access Management) service.

## Prerequisites

- Python 3.13+
- Docker and Docker Compose
- Git

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/NithinM29602/IAM.git
cd IAM
```

### 2. Create and Activate Virtual Environment

Create a Python virtual environment:

```sh
python3 -m venv iam_env
```

Activate the virtual environment:

**On Unix/macOS:**
```sh
source iam_env/bin/activate
```

**On Windows:**
```sh
iam_env\Scripts\activate
```

You should see `(iam_env)` in your terminal prompt, indicating the virtual environment is active.

### 3. Install Dependencies

Install the required packages:

```sh
pip install -r requirements.txt
```

### 4. Start MongoDB with Docker Compose

Make sure Docker is installed and running on your system, then start the required services in detached mode:

```sh
docker-compose up -d
```

This will start MongoDB and any other required services defined in the docker-compose.yaml file.



## API Documentation

Once the service is running, you can access the interactive API documentation at:

- Swagger UI: [http://localhost:8081/iam/v1/docs](http://localhost:8081/iam/v1/docs)

These interfaces allow you to:
- Browse available endpoints
- See required request parameters and response formats
- Test API calls directly from the browser



## Stopping the Application

2. To stop the Docker services:
   ```sh
   docker-compose down
   ```

3. To deactivate the virtual environment:
   ```sh
   deactivate
   ```



## File Structure

```
.
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       └── users.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── rate_limit.py
│   │   └── security.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── schemas.py
│   ├── dependencies
│   │   └── db.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── token.py
│   │   └── user.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── user_service.py
│   └── utils
│       ├── __init__.py
│       ├── exception_handler.py
│       └── logger.py
├── docker-compose.yaml
├── Dockerfile
├── docs
│   ├── api
│   │   └── openapi.json
│   └── architecture
├── README.md
├── requirements.txt
└── tests
    ├── __init__.py
    ├── test_auth.py
    └── test_users.py

```