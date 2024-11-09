from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..exceptions import (
    DatabaseError,
    InvalidDataError,
    ResourceConflict,
    ResourceNotFound,
)
from .repository import (
    create_user,
    delete_user,
    get_all_users,
    get_user,
    get_user_by_email,
    update_user,
)
from .schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a user by their ID."""
    try:
        db_user = await get_user(db, user_id=user_id)
        return db_user
    except ResourceNotFound:
        raise
    except SQLAlchemyError:
        raise DatabaseError()


@router.get("/email/{email}", response_model=UserResponse)
async def read_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """Retrieve a user by their email."""
    try:
        db_user = await get_user_by_email(db, email=email)
        return db_user
    except ResourceNotFound:
        raise
    except SQLAlchemyError:
        raise DatabaseError()


@router.get("/", response_model=list[UserResponse])
async def read_all_users(db: AsyncSession = Depends(get_db)):
    """Retrieve all users."""
    try:
        users = await get_all_users(db)
        return users
    except SQLAlchemyError:
        raise DatabaseError("Failed to retrieve users.")


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user."""
    try:
        db_user = await get_user_by_email(db, email=user.email)
        if db_user:
            raise ResourceConflict(resource="User", message="Email already registered")
        return await create_user(db=db, user=user)
    except ResourceConflict:
        raise
    except SQLAlchemyError:
        raise DatabaseError()
    except ValueError:
        raise InvalidDataError(message="Invalid user data provided.")


@router.patch("/{user_id}", response_model=UserResponse)
async def update_existing_user(
    user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a user's information."""
    try:
        db_user = await update_user(
            db, user_id, user_data.model_dump(exclude_unset=True)
        )
        return db_user
    except ResourceNotFound:
        raise
    except SQLAlchemyError:
        raise DatabaseError("Failed to update user.")
    except ValueError:
        raise InvalidDataError(message="Invalid data provided.")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a user by their ID."""
    try:
        await delete_user(db, user_id)
        return {"message": "User deleted successfully"}
    except ResourceNotFound:
        raise
    except SQLAlchemyError:
        raise DatabaseError("Failed to delete user.")
