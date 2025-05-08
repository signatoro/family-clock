
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.types import JSON
from sqlalchemy.dialects.postgresql import ARRAY
from app.src.util.db import Base
import json

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)

    hashed_password = Column(String, nullable=False)

    # Store group lists as JSON strings (SQLite-friendly)
    owned_groups_list = Column(Text, default="[]")
    joined_groups_list = Column(Text, default="[]")
    pending_group_list = Column(Text, default="[]")