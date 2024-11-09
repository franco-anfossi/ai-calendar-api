from typing import Optional

from pydantic import BaseModel


class CalendarBase(BaseModel):
    name: str
    color: Optional[str] = None


class CalendarCreate(CalendarBase):
    user_id: int


class CalendarUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None


class CalendarResponse(CalendarBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
