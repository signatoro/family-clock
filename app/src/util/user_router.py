# app/src/util/auth_router.py
from fastapi import Depends
from app.src.util.auth import get_current_user
from fastapi import APIRouter
from enum import Enum

class UserAPIRouter(APIRouter):
    def __init__(self, tags: list[str | Enum] | None = None, prefix: str = "", **kwargs):
        super().__init__(tags=tags, prefix=prefix, dependencies=[Depends(get_current_user)], **kwargs)
