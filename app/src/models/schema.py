from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field



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