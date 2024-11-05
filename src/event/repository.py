from models import Event
from schemas import EventCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(Event).filter(Event.id == event_id))
    return result.scalar_one_or_none()


async def get_events_by_calendar(db: AsyncSession, calendar_id: int):
    result = await db.execute(select(Event).filter(Event.calendar_id == calendar_id))
    return result.scalars().all()


async def create_event(db: AsyncSession, event: EventCreate):
    db_event = Event(
        title=event.title,
        description=event.description,
        start_datetime=event.start_datetime,
        end_datetime=event.end_datetime,
        calendar_id=event.calendar_id,
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event
