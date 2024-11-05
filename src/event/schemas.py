from datetime import datetime

from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: str = None
    start_datetime: datetime
    end_datetime: datetime


class EventCreate(EventBase):
    calendar_id: int  # ID del calendario al que pertenece el evento


class EventResponse(EventBase):
    id: int
    calendar_id: int

    class Config:
        orm_mode = (
            True  # Permite que Pydantic use objetos SQLAlchemy para las respuestas
        )
