from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext
from app.utils.logger import get_logger

logger = get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
        subject: Union[str, Any],
        expires_delta: Optional[timedelta] = None,
        is_admin: bool = False,
) -> str:
    """
    Create an access token using the provided data.

    Args:
        subject (Union[str, Any]): The subject for the token.
        expires_delta (Optional[datetime.timedelta]): The expiration time for the token.
        is_admin (bool): Indicates if the user is an admin.

    Returns:
        str: The encoded access token.
    """
    logger.info("Creating access token...")
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)

    to_encode = {"exp": expire, "sub": str(subject), "admin": is_admin}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    logger.info(f"Access token created successfully --> {encoded_jwt}")
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    logger.info("Verifying password...")
    if not plain_password or not hashed_password:
        logger.error("Password verification failed: empty password")
        return False
    result = pwd_context.verify(plain_password, hashed_password)
    logger.info(f"Password verification result: {result}")
    return result

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    logger.info("Hashing password...")
    hashed_password = pwd_context.hash(password)
    logger.info(f"Password hashed successfully --> {hashed_password}")
    return hashed_password
