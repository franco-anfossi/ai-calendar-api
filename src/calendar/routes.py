from fastapi import APIRouter, Depends, HTTPException
from repository import create_calendar, get_calendar, get_calendars_by_user
from schemas import CalendarCreate, CalendarResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db

router = APIRouter(prefix="/calendars", tags=["calendars"])


@router.get("/{calendar_id}", response_model=CalendarResponse)
async def read_calendar(calendar_id: int, db: AsyncSession = Depends(get_db)):
    db_calendar = await get_calendar(db, calendar_id=calendar_id)
    if db_calendar is None:
        raise HTTPException(status_code=404, detail="Calendar not found")
    return db_calendar


@router.get("/user/{user_id}", response_model=list[CalendarResponse])
async def read_calendars_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_calendars_by_user(db, user_id=user_id)


@router.post("/", response_model=CalendarResponse)
async def create_new_calendar(
    calendar: CalendarCreate, db: AsyncSession = Depends(get_db)
):
    return await create_calendar(db=db, calendar=calendar)
