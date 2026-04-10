from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(settings.database_url,
                                     echo=False,
                                     pool_size=20,
                                     max_overflow=20,
                                     pool_timeout=60,
                                     pool_recycle=3600
                                     )

SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_= AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as session:
        yield session