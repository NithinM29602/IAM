from typing import Optional
from app.models.user import UserInDB, UserCreate
from app.core.security import get_password_hash
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import HTTPException
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def create_user(user_info: UserCreate, user_collections: AsyncIOMotorCollection) -> UserInDB:
    """
    Create a new user in the system.

    Args:
        user_info (UserCreate): The user information to create.

    Returns:
        UserInDB: The created user object.
    """
    logger.info("Creating user...")
    existing_user = await get_user_by_email(user_info.email, user_collections)
    if existing_user:
        logger.error("Email already registered, Please use another email")
        raise HTTPException(
            status_code=400,
            detail="Email already registered, Please use another email"
        )
    try:
        logger.info("Hashing password...")
        hashed_password = get_password_hash(user_info.password)
        user_data = user_info.dict()
        del user_data["password"]

        logger.info("Adding user to a database...")
        db_user = UserInDB(
            **user_data,
            hashed_password=hashed_password,
        )

        inserted_user = await user_collections.insert_one(db_user.dict(by_alias=True))
        db_user.id = str(inserted_user.inserted_id)
        logger.info(f"User created successfully with ID: {db_user.id}")
        logger.info(f"User details: {db_user}")
        return db_user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

async def get_user_by_email(email: str, user_collections: AsyncIOMotorCollection) -> Optional[UserInDB]:
    """
    Args:
        email (str): The email of the user to retrieve.
        user_collections (AsyncIOMotorCollection): The MongoDB collection for users.
    Returns:
        UserInDB: The user object if found, None otherwise.
    """
    logger.info(f"Retrieving user by email: {email}")
    if user_data := await user_collections.find_one({"email": email}):
        logger.info(f"User details: {user_data}")
        return UserInDB(**user_data)
    logger.info("User not found.")
    return None

async def get_user_by_id(user_id: str, user_collections: AsyncIOMotorCollection) -> Optional[UserInDB]:
    """
    Args:
        user_id (str): The ID of the user to retrieve.
        user_collections (AsyncIOMotorCollection): The MongoDB collection for users.
    Returns:
        UserInDB: The user object if found, None otherwise.
    """
    logger.info(f"Retrieving user by ID: {user_id}")
    if user_data := await user_collections.find_one({"_id": user_id}):
        logger.info(f"User details: {user_data}")
        return UserInDB(**user_data)
    logger.info("User not found.")
    return None
