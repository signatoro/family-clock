
from sqlalchemy import select
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm


from app.src.util.db import get_db
from app.src.models.schema import Token
from app.src.models.schema import User, UserDB
from app.src.controller.user_controller import UserController
from app.src.util.auth import get_current_user, hash_password
from app.src.util.auth import verify_password, create_access_token, create_refresh_token, oauth2_scheme


class UserEndpoints():
    router: APIRouter = APIRouter(
        prefix='/user',
        tags=['user']
    )


    def __init__(self, controller: UserController):
        self.controller = controller

        self.router.add_api_route('/create', self.create_new_user, methods=["POST"])
        self.router.add_api_route('/token', self.read_users_me, methods=['GET'])
        # self.router.add_api_route('/whoami', self.who_am_i, methods=['GET'])

        # self.router.add_api_route('/login', self.login, methods=['POST'])

    
    async def create_new_user(self, user: User, password: str, db: AsyncSession = Depends(get_db)):
        # # Check if user already exists
        # existing = await self.controller.get_user_by_email(db, user.email)
        # if existing:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists.")
    
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

    async def read_users_me(self, token: str = Depends(oauth2_scheme)):
        return {"token": token}
    

    # async def who_am_i(self, current_user: UserDB = Depends(get_current_user)):
    #     return {
    #         "username": current_user.username,
    #         "email": current_user.email,
    #         "phone_number": current_user.phone_number,
    # }

    
    # async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    #     result = await db.execute(select(UserDB).where(UserDB.username == form_data.username))
    #     user = result.scalar_one_or_none()

    #     if not user or not verify_password(form_data.password, user.hashed_password):
    #         raise HTTPException(status_code=400, detail="Incorrect username or password")

    #     access_token = create_access_token(data={"sub": user.username})
    #     refresh_token = create_refresh_token(data={"sub": user.username})

    #     user.refresh_token = refresh_token
    #     await db.commit()

    #     return {
    #         "access_token": access_token,
    #         "refresh_token": refresh_token,
    #         "token_type": "bearer"
    #     }
