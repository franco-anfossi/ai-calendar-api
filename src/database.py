from databases import Database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

from .calendar.models import Calendar  # noqa
from .event.models import Event  # noqa
from .user.models import User  # noqa

async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

database = Database(DATABASE_URL)


async def get_db():
    async with async_session() as session:
        yield session
        await session.close()
