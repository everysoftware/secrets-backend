from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from domain.config import domain_settings
from .config import infrastructure_settings

async_engine = create_async_engine(
    url=infrastructure_settings.db.dsn,
    echo=domain_settings.environment.is_debug,
    pool_pre_ping=True,
)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
