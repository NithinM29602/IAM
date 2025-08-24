# IAM Service Architecture

## Overview
This document describes the architecture of the IAM Service.

## Components
- **API Layer**: HTTP endpoints and request handling
- **Service Layer**: Business logic implementation  
- **Data Layer**: Database models and operations
- **Core Layer**: Configuration, security, and utilities

## Security Model
- JWT-based authentication
- Role-based access control (RBAC)
- Password hashing with bcrypt
- Rate limiting protection
