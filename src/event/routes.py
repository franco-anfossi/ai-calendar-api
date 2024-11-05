from fastapi import APIRouter, Depends, HTTPException
from repository import create_event, get_event, get_events_by_calendar
from schemas import EventCreate, EventResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/{event_id}", response_model=EventResponse)
async def read_event(event_id: int, db: AsyncSession = Depends(get_db)):
    db_event = await get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.get("/calendar/{calendar_id}", response_model=list[EventResponse])
async def read_events_by_calendar(calendar_id: int, db: AsyncSession = Depends(get_db)):
    return await get_events_by_calendar(db, calendar_id=calendar_id)


@router.post("/", response_model=EventResponse)
async def create_new_event(event: EventCreate, db: AsyncSession = Depends(get_db)):
    return await create_event(db=db, event=event)
