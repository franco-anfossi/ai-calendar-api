from models import Calendar
from schemas import CalendarCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_calendar(db: AsyncSession, calendar_id: int):
    result = await db.execute(select(Calendar).filter(Calendar.id == calendar_id))
    return result.scalar_one_or_none()


async def get_calendars_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Calendar).filter(Calendar.user_id == user_id))
    return result.scalars().all()


async def create_calendar(db: AsyncSession, calendar: CalendarCreate):
    db_calendar = Calendar(
        name=calendar.name, color=calendar.color, user_id=calendar.user_id
    )
    db.add(db_calendar)
    await db.commit()
    await db.refresh(db_calendar)
    return db_calendar
