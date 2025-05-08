# app/tests/conftest.py

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.src.util.db import Base
from app.src.models.schema import UserDB  # Assuming this is your model from Pydantic
import bcrypt

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
