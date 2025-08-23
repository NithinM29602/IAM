from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserCreate, User
from app.models.token import Token, LoginCredentials
from app.services.user_service import create_user
from app.services.auth_service import authenticate_user, create_token
from app.dependencies.db import get_user_collections
from motor.motor_asyncio import AsyncIOMotorCollection
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/signIn", response_model=Token)
async def sign_in(
    credentails: LoginCredentials,
    user_collections: AsyncIOMotorCollection = Depends(get_user_collections)
):
    """
    Sign in a user and return a token.
    
    Args:
        credentails (LoginCredentials): The user's credentials containing email and password.

    Returns:
        Token: The token for the authenticated user.
    """
    
    logger.info("Inside a signIn.")
    email = credentails.email
    password = credentails.password
    user = await authenticate_user(email=email, password=password, user_collections=user_collections)
    if not user:
        logger.error(f"Invalid credentials for email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if not user.is_active:
        logger.error("Inactive user")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    access_token = await create_token(
        user_id=user.id,
        is_admin=user.is_admin
    )
    return access_token

@router.post("/signUp", response_model=User)
async def sign_up(
    user_info: UserCreate,
    user_collections: AsyncIOMotorCollection = Depends(get_user_collections)
):
    """
    Sign up a new user and return a token.

    Args:
        user_info (UserCreate): The user information to create.

    Returns:
        Token: The token for the newly created user.
    """
    logger.info("Inside a signUp.")
    user = await create_user(user_info, user_collections)
    return User(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_admin=user.is_admin,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


