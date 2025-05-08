# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
# import os

# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# # Set check_same_thread=False for SQLite only
# engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
# )

# # Use scoped_session for thread safety (especially in web apps)
# SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base = declarative_base()

# # Dependency (for FastAPI or manual use)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./familyclock.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session