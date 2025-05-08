from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict

class User(BaseModel):
    username: str
    email: Optional[EmailStr]
    phone_number: Optional[str]
    disabled: bool = False


class UserDB(User):
    hashed_password: str

    owned_groups_list: List[int] = Field(default_factory=list)
    joined_groups_list: List[int] = Field(default_factory=list)
    pending_group_list: List[int] = Field(default_factory=list)