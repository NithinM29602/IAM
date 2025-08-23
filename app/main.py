from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.api.v1 import auth
from app.core.config import settings
from app.db.database import mongodb
from app.utils.logger import get_logger
from fastapi.exceptions import RequestValidationError
from app.utils.exception_handler import validation_exception_handler

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event to connect and disconnect from the database."""
    logger.info("Connecting to MongoDB...")
    await mongodb.connect()
    logger.info("Connected to MongoDB.")
    yield
    logger.info("Disconnecting from MongoDB and closing the connection...")
    await mongodb.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    lifespan=lifespan,
)


# Initialize the Custom Exception Handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8081, log_level="info")