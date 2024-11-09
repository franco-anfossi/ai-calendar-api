from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..exceptions import DatabaseError, ResourceConflict, ResourceNotFound
from .models import User
from .schemas import UserCreate


async def get_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(User).filter(User.id == user_id))
        db_user = result.scalar_one_or_none()
        if db_user is None:
            raise ResourceNotFound(resource="User")
        return db_user
    except SQLAlchemyError:
        raise DatabaseError()


async def get_user_by_email(db: AsyncSession, email: str):
    try:
        result = await db.execute(select(User).filter(User.email == email))
        db_user = result.scalar_one_or_none()
        if db_user is None:
            raise ResourceNotFound(resource="User")
        return db_user
    except SQLAlchemyError:
        raise DatabaseError()


async def get_all_users(db: AsyncSession):
    """Retrieve all users from the database."""
    try:
        result = await db.execute(select(User))
        return result.scalars().all()
    except SQLAlchemyError:
        raise DatabaseError("Failed to retrieve users.")


async def create_user(db: AsyncSession, user: UserCreate):
    """Create a new user in the database."""
    db_user = User(email=user.email, name=user.name)
    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        raise ResourceConflict(
            resource="User", message="A user with this email already exists."
        )
    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Failed to create user.")


async def update_user(db: AsyncSession, user_id: int, updated_data: dict):
    """Update an existing user with the provided data."""
    try:
        db_user = await get_user(db, user_id)
        for key, value in updated_data.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except ResourceNotFound:
        raise
    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Failed to update user.")


async def delete_user(db: AsyncSession, user_id: int):
    """Delete a user from the database, ensuring cascade deletion."""
    try:
        db_user = await get_user(db, user_id)
        await db.delete(db_user)
        await db.commit()
        return {"message": "User deleted successfully"}
    except ResourceNotFound:
        raise
    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Failed to delete user.")
