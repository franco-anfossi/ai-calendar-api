from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime


class EventCreate(EventBase):
    calendar_id: int  # ID del calendario al que pertenece el evento
    user_id: int  # ID del usuario que creó el evento


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None


class EventResponse(EventBase):
    id: int
    calendar_id: int
    user_id: int

    class Config:
        orm_mode = (
            True  # Permite que Pydantic use objetos SQLAlchemy para las respuestas
        )
