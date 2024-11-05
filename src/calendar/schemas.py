from pydantic import BaseModel


class CalendarBase(BaseModel):
    name: str
    color: str = None


class CalendarCreate(CalendarBase):
    user_id: int


class CalendarResponse(CalendarBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
