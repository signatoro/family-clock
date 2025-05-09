
import pytest
import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.models.schema import UserDB
from app.src.controller import user_controller
from app.src.models import schema as user_schema


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
async def test_get_user_by_email(db, sample_user):
    controller:user_controller.UserController = user_controller.UserController()
    # Setup
    await controller.create_user(db, sample_user)

    # Act
    fetched = await controller.get_user_by_email(db, sample_user.email)

    # Assert
    assert fetched is not None
    assert fetched.username == sample_user.username
    assert fetched.email == sample_user.email

    await db.rollback()

@pytest.mark.asyncio
async def test_get_user_by_email_returns_none_when_not_found(db):
    controller:user_controller.UserController = user_controller.UserController()

    fetched = await controller.get_user_by_email(db, "nonexistent@example.com")
    assert fetched is None

    await db.rollback()

@pytest.mark.asyncio
async def test_create_user_duplicate_username_raises(db, sample_user):
    controller:user_controller.UserController = user_controller.UserController()

    await controller.create_user(db, sample_user)
    with pytest.raises(IntegrityError):
        await controller.create_user(db, sample_user)
    
    await db.rollback()

@pytest.mark.asyncio
async def test_create_user_duplicate_email_raises(db, sample_users, sample_user):
    controller:user_controller.UserController = user_controller.UserController()

    for user in sample_users:
        await controller.create_user(db, user)
    
    with pytest.raises(IntegrityError):
        await controller.create_user(db, UserDB(
            username="testuser",
            email="test@example.com",
            phone_number="555-1234",
            disabled=False,
            hashed_password=bcrypt.hashpw("testpass".encode(), bcrypt.gensalt()).decode(),
            owned_groups_list=[1],
            joined_groups_list=[2],
            pending_group_list=[3],
        ))
    
    await db.rollback()

@pytest.mark.asyncio
async def test_create_user_duplicate_phone_number(db, sample_users):
    controller:user_controller.UserController = user_controller.UserController()

    for user in sample_users:
        await controller.create_user(db, user)

    new_user = UserDB(
        username="testusernew",
        email="testnew@example.com",
        phone_number="555-1234",
        disabled=False,
        hashed_password=bcrypt.hashpw("testpass".encode(), bcrypt.gensalt()).decode(),
        owned_groups_list=[1],
        joined_groups_list=[2],
        pending_group_list=[3],
    )
    
    created = await controller.create_user(db, new_user)

    assert created.username == 'testusernew'
    assert created.email == "testnew@example.com"
    assert created.phone_number == "555-1234"

    await db.rollback()

