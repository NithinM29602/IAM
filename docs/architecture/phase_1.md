
# IAM Authentication Engine

This project implements an **Identity and Access Management (IAM) Authentication Engine**.  
It supports **Root User** and **IAM User** creation, management, and authentication.

---

## Features

- Root User Sign-up & Authentication
- IAM User Sign-up & Authentication
- CRUD operations on Root and IAM Users
- Unique **Account ID** per Root User
- Unique **KRN** (Krutrim Resource Name) per user
- Secure Password Hashing
- MongoDB Storage

---

## Why Account ID is Needed?

- The **Account ID** acts like the **house number** of a tenant.  
- A root user owns the account, and IAM users belong to that account.  
- If a person is part of multiple tenants (e.g., works in multiple organizations), then **Account ID helps us know under which tenant he is trying to authenticate**.

**Real-World Example:**  
Imagine Gmail.  
- Your **Google Account (Root User)** is identified by a unique **Google Account ID**.  
- You might have access to multiple Google Cloud projects (IAM Users).  
- To log in to a project, you need both **Account ID (which project/org you are logging into)** + **your email/password**.

Without Account ID, the system won’t know *which tenant’s login context* you are in.

---

## Data Models

### Root User

When a Root User signs up, the following fields are stored:

- **uuid**: Unique identifier (UUIDv4)
- **accountId**: Unique Account ID for the root account
- **email**: Root user's email (unique)
- **password**: Hashed password
- **firstName**
- **lastName**
- **krn**: krn:iam:<account-id>:users:<uuid>
- **isDeleted**: false
- **isRoot**: true
- **createdAt**
- **updatedAt**

### IAM User

When an IAM User signs up (requires Root User token), the following fields are stored:

- **uuid**: Unique identifier (UUIDv4)
- **accountId**: Parent Root User’s Account ID
- **email**: IAM user email (unique within account)
- **password**: Hashed password
- **firstName**
- **lastName**
- **krn**: krn:iam:<account-id>:users:<uuid>
- **isDeleted**: false
- **isRoot**: false
- **createdAt**
- **updatedAt**

---

## KRN Format

```
krn:<service-name>:<account-id>:users:<user-uuid>
```

Examples:
- Root User: `krn:iam:123456789:user:a1b2c3d4`
- IAM User: `krn:iam:123456789:users:e5f6g7h8`

---

## API Endpoints

## Root Auth

- **POST /iam/v1/SignUpAsRootUser** → Create root user (requires `email`, `password`)
- **POST /iam/v1/SignInAsRootUser** → Authenticate root user


## IAM Auth

- **POST /iam/v1/SignUpAsIAMUser** → Create IAM user (requires `rootToken`, `accountId`, `email`, `password`)
- **POST /iam/v1/SignInAsIAMUser** → Authenticate IAM user


## Common User Management (Root + IAM)

- **GET /iam/v1/users/{userId}** → Fetch user details
- **PUT /iam/v1/users/{userId}** → Update user details
- **DELETE /iam/v1/users/{userId}** → Deactivate user

---

## Workflow

1. Root User signs up → generates `accountId` and root `krn`
2. Root User logs in → gets access token
3. IAM User sign-up → requires root token, generates IAM user `krn`
4. Both Root and IAM users can be managed via CRUD APIs

---

## Example MongoDB Documents

### 1. Root User Sign Up
**Request (JSON):**
```json
{
  "email": "admin@example.com",
  "password": "SecurePass123",
  "firstName": "Alice",
  "lastName": "Johnson"
}
```

**DB Entry (MongoDB):**
```json
{
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "accountId": "123456789",
  "email": "root@example.com",
  "password": "<hashed-password>",
  "firstName": "Alice",
  "lastName": "Admin",
  "krn": "krn:iam:123456789:users:550e8400-e29b-41d4-a716-446655440000",
  "status": "active",
  "isRoot": true,
  "createdAt": "2025-08-24T12:00:00Z",
  "updatedAt": "2025-08-24T12:00:00Z"
}
```

### 2. IAM User Sign Up
**Request (JSON):**
```json
{
  "accountId": "acc-123456",
  "email": "dev@example.com",
  "password": "DevPass456",
  "firstName": "Bob",
  "lastName": "Smith"
}
```

**DB Entry (MongoDB):**
```json
{
  "uuid": "660e8400-e29b-41d4-a716-446655440000",
  "accountId": "123456789",
  "email": "iam@example.com",
  "password": "<hashed-password>",
  "firstName": "Bob",
  "lastName": "User",
  "krn": "krn:iam:123456789:users:660e8400-e29b-41d4-a716-446655440000",
  "status": "active",
  "isRoot": false,
  "createdAt": "2025-08-24T12:10:00Z",
  "updatedAt": "2025-08-24T12:10:00Z"
}
```

---

## Examples


**Sign In (Root User):**
```json
{
  "email": "admin@example.com",
  "password": "SecurePass123"
}
```

**Sign In (IAM User):**
```json
{
  "accountId": "287123456",
  "email": "dev@example.com",
  "password": "DevPass456"
}
```

---

## Team Responsibilities

- **Person 1**: Root User APIs (Sign-up, Login, CRUD)
- **Person 2**: IAM User APIs (Sign-up, Login, CRUD)

---

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Auth**: JWT (JSON Web Token)
- **Hashing**: bcrypt / argon2

---
