from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config.config import settings

# асинхронный движок
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    # echo=True,
)

# асинхронное подключение к бд
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
