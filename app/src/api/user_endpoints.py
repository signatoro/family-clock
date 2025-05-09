
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.util.db import get_db
from app.src.util.auth import hash_password
from app.src.models.schema import User, UserDB
from app.src.controller.user_controller import UserController
from app.src.util.auth import create_access_token, create_refresh_token, oauth2_scheme


class UserEndpoints():
    router: APIRouter = APIRouter(
        prefix='/user',
        tags=['user']
    )


    def __init__(self, controller: UserController):
        self.controller = controller

        self.router.add_api_route('/create', self.create_new_user, methods=["POST"])
    
    async def create_new_user(self, user: User, password: str, db: AsyncSession = Depends(get_db)):
    
        userdb = UserDB(
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            disabled=user.disabled,
            hashed_password= hash_password(password),  
            owned_groups_list=[],
            joined_groups_list=[],
            pending_group_list=[],
        )
        await self.controller.create_user(db, user=userdb)

        # Generate tokens
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "username": user.username,
                "email": user.email
            }
        }

    