from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    calendars = relationship(
        "Calendar", back_populates="user", cascade="all, delete-orphan"
    )
