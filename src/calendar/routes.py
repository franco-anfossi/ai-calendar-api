from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..exceptions import DatabaseError, ResourceNotFound
from .repository import (
    create_calendar,
    delete_calendar,
    get_all_calendars,
    get_calendar,
    get_calendars_by_user,
    update_calendar,
)
from .schemas import CalendarCreate, CalendarResponse, CalendarUpdate
from .services import import_ics

router = APIRouter(prefix="/calendars", tags=["calendars"])


@router.get("/", response_model=list[CalendarResponse])
async def read_all_calendars(db: AsyncSession = Depends(get_db)):
    """Retrieve all calendars."""
    try:
        return await get_all_calendars(db)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{calendar_id}", response_model=CalendarResponse)
async def read_calendar(calendar_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a single calendar by its ID."""
    try:
        return await get_calendar(db, calendar_id=calendar_id)
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Calendar not found")
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Failed to retrieve calendar.")


@router.get("/user/{user_id}", response_model=list[CalendarResponse])
async def read_calendars_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve all calendars for a specific user."""
    try:
        return await get_calendars_by_user(db, user_id=user_id)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=CalendarResponse, status_code=201)
async def create_new_calendar(
    calendar: CalendarCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new calendar."""
    try:
        return await create_calendar(db=db, calendar=calendar)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{calendar_id}", response_model=CalendarResponse)
async def update_existing_calendar(
    calendar_id: int, calendar_data: CalendarUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a calendar's information."""
    try:
        return await update_calendar(db, calendar_id, calendar_data)
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Calendar not found")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{calendar_id}", status_code=204)
async def delete_existing_calendar(
    calendar_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete a calendar by its ID."""
    try:
        await delete_calendar(db, calendar_id)
        return {"message": "Calendar deleted successfully"}
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Calendar not found")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import", status_code=201)
async def import_calendar_ics(
    file: UploadFile = File(...),
    user_id: int = Form(
        ...
    ),  # Se requiere el user_id para asignar el calendario al usuario
    calendar_id: int = Form(None),  # calendar_id opcional
    db: AsyncSession = Depends(get_db),
):
    """Import a .ics file to a calendar."""
    try:
        response = await import_ics(await file.read(), user_id, db, calendar_id)
        return response
    except ResourceNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
