from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..exceptions import DatabaseError, ResourceNotFound
from .repository import (
    create_event,
    delete_event,
    get_all_events,
    get_event,
    get_events_by_calendar,
    get_events_by_user,
    update_event,
)
from .schemas import EventCreate, EventResponse, EventUpdate

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/{event_id}", response_model=EventResponse)
async def read_event(event_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a single event by its ID."""
    try:
        return await get_event(db, event_id=event_id)
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Event not found")
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Failed to retrieve event.")


@router.get("/user/{user_id}", response_model=list[EventResponse])
async def read_events_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve all events for a specific user."""
    try:
        return await get_events_by_user(db, user_id=user_id)
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="No events found for this user.")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calendar/{calendar_id}", response_model=list[EventResponse])
async def read_events_by_calendar(calendar_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve all events for a specific calendar."""
    try:
        return await get_events_by_calendar(db, calendar_id=calendar_id)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[EventResponse])
async def read_all_events(db: AsyncSession = Depends(get_db)):
    """Retrieve all events."""
    try:
        return await get_all_events(db)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=EventResponse, status_code=201)
async def create_new_event(event: EventCreate, db: AsyncSession = Depends(get_db)):
    """Create a new event."""
    try:
        return await create_event(db=db, event=event)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{event_id}", response_model=EventResponse)
async def update_existing_event(
    event_id: int, event_data: EventUpdate, db: AsyncSession = Depends(get_db)
):
    """Update an event's information."""
    try:
        return await update_event(db, event_id, event_data)
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Event not found")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{event_id}", status_code=204)
async def delete_existing_event(event_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an event by its ID."""
    try:
        await delete_event(db, event_id)
        return {"message": "Event deleted successfully"}
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Event not found")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
