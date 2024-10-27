from core.configs import settings
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

engine: AsyncEngine = create_async_engine(settings.DB_URL)


Session: AsyncSession = sessionmaker(
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
