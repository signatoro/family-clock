# app/tests/conftest.py

import json
import secrets
import string
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.src.util.db import Base

import bcrypt

from app.src.models import user as user_model
from app.src.models.schema import UserDB 


# In-memory SQLite for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"  

# Async DB engine and session maker
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@pytest_asyncio.fixture
async def db():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    await engine.dispose()

@pytest.fixture
def sample_raw_user() -> user_model.User:
    db_user = user_model.User(
        username="testuser",
        email="test@example.com",
        phone_number="555-1234",
        disabled=False,
        hashed_password='hased',
        owned_groups_list=json.dumps([]),
        joined_groups_list=json.dumps([]),
        pending_group_list=json.dumps([]),
    )
    return db_user

@pytest.fixture
def sample_passwords(count=20, length=14) -> list[str]:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return [ ''.join(secrets.choice(alphabet) for _ in range(length)) for _ in range(count) ]

@pytest.fixture
def sample_user() -> UserDB:
    """Fixture for creating a sample user."""
    hashed_pw = bcrypt.hashpw("testpass".encode(), bcrypt.gensalt()).decode()
    return UserDB(
        username="testuser",
        email="test@example.com",
        phone_number="555-1234",
        disabled=False,
        hashed_password=hashed_pw,
        owned_groups_list=[1],
        joined_groups_list=[2],
        pending_group_list=[3],
    )

@pytest.fixture
def sample_users() -> list[UserDB]:
    """Fixture for creating a sample user."""
    hashed_pw = bcrypt.hashpw("testpass".encode(), bcrypt.gensalt()).decode()
    users: list[UserDB] = []
    users.append(UserDB(
        username="testuser",
        email="test@example.com",
        phone_number="555-1234",
        disabled=False,
        hashed_password=hashed_pw,
        owned_groups_list=[1],
        joined_groups_list=[2],
        pending_group_list=[3],
    ))

    users.append(UserDB(
        username="testuser0",
        email="test0@example.com",
        phone_number="555-1236",
        disabled=False,
        hashed_password=bcrypt.hashpw("testpass0".encode(), bcrypt.gensalt()).decode(),
        owned_groups_list=[1],
        joined_groups_list=[2],
        pending_group_list=[3],
    ))

    users.append(UserDB(
        username="testuser1",
        email="test1@example.com",
        phone_number="555-1235",
        disabled=False,
        hashed_password=bcrypt.hashpw("testpass1".encode(), bcrypt.gensalt()).decode(),
        owned_groups_list=[1],
        joined_groups_list=[2],
        pending_group_list=[3],
    ))

    users.append(UserDB(
        username="testuser2",
        email="test2@example.com",
        phone_number="555-1233",
        disabled=False,
        hashed_password=bcrypt.hashpw("testpass2".encode(), bcrypt.gensalt()).decode(),
        owned_groups_list=[1],
        joined_groups_list=[2],
        pending_group_list=[3],
    ))

    return users
