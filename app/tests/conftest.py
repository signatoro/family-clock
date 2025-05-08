import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.src.util.db import Base
from app.src.models import schema as user_schema
import bcrypt

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_user() -> user_schema.UserDB:
    hashed_pw = bcrypt.hashpw("testpass".encode(), bcrypt.gensalt()).decode()
    return user_schema.UserDB(
        username="testuser",
        email="test@example.com",
        phone_number="555-1234",
        disabled=False,
        hashed_password=hashed_pw,
        owned_groups_list=[1],
        joined_groups_list=[2],
        pending_group_list=[3],
    )
