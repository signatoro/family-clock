from app.src.controller import user_controller
from app.src.models import schema as user_schema
from sqlalchemy.exc import IntegrityError
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.src.models.schema import UserDB

@pytest.mark.asyncio
async def test_create_user(db: AsyncSession, sample_user: UserDB):
    controller:user_controller.UserController = user_controller.UserController()

    created = await controller.create_user(db, sample_user)
    assert created.username == sample_user.username
    assert created.email == sample_user.email
    assert created.phone_number == sample_user.phone_number

    await db.rollback()

@pytest.mark.asyncio
async def test_get_user_by_username(db, sample_user):
    controller:user_controller.UserController = user_controller.UserController()
    # Setup
    await controller.create_user(db, sample_user)

    # Act
    fetched = await controller.get_user_by_username(db, sample_user.username)

    # Assert
    assert fetched is not None
    assert fetched.username == sample_user.username

    await db.rollback()

@pytest.mark.asyncio
async def test_get_user_by_username_returns_none_when_not_found(db):
    controller:user_controller.UserController = user_controller.UserController()

    fetched = await controller.get_user_by_username(db, "nonexistent")
    assert fetched is None

    await db.rollback()

@pytest.mark.asyncio
async def test_create_user_duplicate_username_raises(db, sample_user):
    controller:user_controller.UserController = user_controller.UserController()

    await controller.create_user(db, sample_user)
    with pytest.raises(IntegrityError):
        await controller.create_user(db, sample_user)
    
    await db.rollback()
