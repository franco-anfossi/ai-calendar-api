from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..exceptions import DatabaseError, ResourceNotFound
from .models import Event
from .schemas import EventCreate, EventUpdate


async def get_event(db: AsyncSession, event_id: int):
    try:
        result = await db.execute(select(Event).filter(Event.id == event_id))
        db_event = result.scalar_one_or_none()
        if db_event is None:
            raise ResourceNotFound(resource="Event")
        return db_event
    except SQLAlchemyError:
        raise DatabaseError()


async def get_events_by_user(db: AsyncSession, user_id: int):
    """Retrieve all events for a specific user."""
    try:
        result = await db.execute(select(Event).filter(Event.user_id == user_id))
        events = result.scalars().all()
        if not events:
            raise ResourceNotFound(resource="Events for the specified user")
        return events
    except SQLAlchemyError:
        raise DatabaseError("Failed to retrieve events for the user.")


async def get_events_by_calendar(db: AsyncSession, calendar_id: int):
    try:
        result = await db.execute(
            select(Event).filter(Event.calendar_id == calendar_id)
        )
        return result.scalars().all()
    except SQLAlchemyError:
        raise DatabaseError("Failed to retrieve events by calendar.")


async def get_all_events(db: AsyncSession):
    """Retrieve all events."""
    try:
        result = await db.execute(select(Event))
        return result.scalars().all()
    except SQLAlchemyError:
        raise DatabaseError("Failed to retrieve events.")


async def create_event(db: AsyncSession, event: EventCreate):
    db_event = Event(
        title=event.title,
        description=event.description,
        start_datetime=event.start_datetime,
        end_datetime=event.end_datetime,
        calendar_id=event.calendar_id,
        user_id=event.user_id,
    )
    try:
        db.add(db_event)
        await db.commit()
        await db.refresh(db_event)
        return db_event
    except IntegrityError:
        await db.rollback()
        raise DatabaseError("Failed to create event due to a database conflict.")
    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Failed to create event.")


async def update_event(db: AsyncSession, event_id: int, event_data: EventUpdate):
    """Update an existing event with the provided data."""
    try:
        db_event = await get_event(db, event_id)
        for key, value in event_data.model_dump(exclude_unset=True).items():
            setattr(db_event, key, value)
        await db.commit()
        await db.refresh(db_event)
        return db_event
    except ResourceNotFound:
        raise
    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Failed to update event.")


async def delete_event(db: AsyncSession, event_id: int):
    """Delete an event from the database."""
    try:
        db_event = await get_event(db, event_id)
        await db.delete(db_event)
        await db.commit()
        return {"message": "Event deleted successfully"}
    except ResourceNotFound:
        raise
    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Failed to delete event.")
