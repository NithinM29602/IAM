from app.services.user_service import get_user_by_email
from app.core.security import verify_password
from app.models.user import UserInDB
from app.models.token import Token
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import timedelta
from app.core.config import settings
from app.core.security import create_access_token
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def authenticate_user(
        email:str,
        password:str,
        user_collections: AsyncIOMotorCollection
) -> Optional[UserInDB]:
    """
    Authenticate a user by checking their username and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    try:
        logger.info("Authenticating user...")
        user = await get_user_by_email(email, user_collections)
        if not user:
            logger.error("User not found")
            return None
        if not verify_password(password, user.hashed_password):
            logger.error("Invalid password")
            return None
        logger.info(f"User authenticated successfully --> {user}")
        return user
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        return None

async def create_token(user_id: str, is_admin: bool = False) -> Token:
    """
    Create a JWT token for the user.

    Args:
        user_id (str): The ID of the user.
        is_admin (bool): Indicates if the user is an admin.

    Returns:
        str: The generated JWT token.
    """
    logger.info("Creating access token...")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    access_token = create_access_token(
        subject=user_id,
        expires_delta=access_token_expires,
        is_admin=is_admin
        )
    return Token(access_token=access_token)