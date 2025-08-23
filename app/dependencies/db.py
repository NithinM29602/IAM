from app.db.database import mongodb
from motor.motor_asyncio import AsyncIOMotorCollection
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def get_user_collections() -> AsyncIOMotorCollection:
    """
    Returns the user collections from the MongoDB database.
    """
    logger.info("Fetching user collections...")
    
    try:
        if not hasattr(mongodb, 'db') or mongodb.db is None:
            # If mongodb.db is not initialized, initialize it
            logger.info("MongoDB connection not initialized, attempting to connect...")
            await mongodb.connect()
            
        logger.info(f"Using collection: {settings.MONGO_COLLECTION_USERINFO}")
        user_collection = mongodb.db[settings.MONGO_COLLECTION_USERINFO]
        return user_collection
    
    except Exception as e:
        logger.error(f"Error accessing MongoDB collection: {str(e)}")
        raise