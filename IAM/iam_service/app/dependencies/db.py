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
    
    # Add error handling to debug the issue
    try:
        if not hasattr(mongodb, 'db') or mongodb.db is None:
            # If mongodb.db is not initialized, initialize it
            logger.info("MongoDB connection not initialized, attempting to connect...")
            await mongodb.connect()
            
        logger.info(f"Using collection: {settings.MONGO_COLLECTION_USERINFO}")
        user_collection = mongodb.db[settings.MONGO_COLLECTION_USERINFO]
        # Try a simple operation to verify the collection is accessible
        count = await user_collection.count_documents({})
        logger.info(f"Collection '{settings.MONGO_COLLECTION_USERINFO}' contains {count} documents")
        return user_collection
    except Exception as e:
        logger.error(f"Error accessing MongoDB collection: {str(e)}")
        # Re-raise or handle the error as appropriate
        raise