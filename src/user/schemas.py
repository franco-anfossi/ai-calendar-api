from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    """Schema for creating a new user."""

    pass


class UserUpdate(BaseModel):
    """Schema for updating user fields selectively."""

    email: Optional[EmailStr] = None
    name: Optional[str] = None


class UserResponse(UserBase):
    """Schema for responses, including the user ID."""

    id: int

    class Config:
        orm_mode = True
