from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..exceptions import DatabaseError, ResourceNotFound
from .models import Calendar
from .schemas import CalendarCreate, CalendarUpdate


async def get_calendar(db: AsyncSession, calendar_id: int):
    try:
        result = await db.execute(select(Calendar).filter(Calendar.id == calendar_id))
        db_calendar = result.scalar_one_or_none()
        if db_calendar is None:
            raise ResourceNotFound(resource="Calendar")
        return db_calendar
    except SQLAlchemyError:
        raise DatabaseError()


async def get_calendars_by_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(Calendar).filter(Calendar.user_id == user_id))
        return result.scalars().all()
    except SQLAlchemyError:
        raise DatabaseError("Failed to retrieve calendars for the user.")


async def get_all_calendars(db: AsyncSession):
    try:
        result = await db.execute(select(Calendar))
        return result.scalars().all()
    except SQLAlchemyError:
        raise DatabaseError("Failed to retrieve calendars.")


async def create_calendar(db: AsyncSession, calendar: CalendarCreate):
    db_calendar = Calendar(
        name=calendar.name, color=calendar.color, user_id=calendar.user_id
    )
    try:
        db.add(db_calendar)
        await db.commit()
        await db.refresh(db_calendar)
        return db_calendar
    except IntegrityError:
        await db.rollback()
        raise DatabaseError("Failed to create calendar due to a database conflict.")
    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Failed to create calendar.")


async def update_calendar(
    db: AsyncSession, calendar_id: int, calendar_data: CalendarUpdate
):
    try:
        db_calendar = await get_calendar(db, calendar_id)
        for key, value in calendar_data.model_dump(exclude_unset=True).items():
            setattr(db_calendar, key, value)
        await db.commit()
        await db.refresh(db_calendar)
        return db_calendar
    except ResourceNotFound:
        raise
    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Failed to update calendar.")


async def delete_calendar(db: AsyncSession, calendar_id: int):
    try:
        db_calendar = await get_calendar(db, calendar_id)
        await db.delete(db_calendar)
        await db.commit()
        return {"message": "Calendar deleted successfully"}
    except ResourceNotFound:
        raise
    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Failed to delete calendar.")
