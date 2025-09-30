#importing the necessary requirements
from .sec import DATABASE_URL
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator
from .model.lms_tables import Users

#normalize aiven url
def normalize_url(url: str) -> str:
    # Convert postgres:// → postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    # Convert postgresql:// → postgresql+asyncpg://
    if url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Remove ?sslmode=require (asyncpg doesn't support it)
    if "sslmode" in url:
        url = url.split("?")[0]

    return url

#async postgres url
ASYNC_DATABASE_URL = normalize_url(DATABASE_URL)

# SQLModel engine
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,  # Optional: set to False in production
    future=True
)
#async session maker
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

#asyn session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            # commit after the endpoint function finishes successfully
            await session.commit()
        except Exception:
            await session.rollback()
            raise


#initialize and create db and tables
async def init_db() -> None:
    async with engine.begin() as conn:
        #print("Running init_db...")  
        await conn.run_sync(SQLModel.metadata.create_all)
        #print("Tables created (if not exist)")