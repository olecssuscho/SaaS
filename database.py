from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings

async_engine = create_async_engine(url = settings.DB_URL, echo = True)

Async_Session = async_sessionmaker(async_engine,autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass