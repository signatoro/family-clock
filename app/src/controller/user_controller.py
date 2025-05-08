import json

import bcrypt
from sqlalchemy import insert
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.models import user as user_model
from app.src.models import schema as user_schema


class UserController():
    async def create_user(self, db: AsyncSession, user: user_schema.UserDB) -> user_model.User:
        db_user = user_model.User(
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            disabled=user.disabled,
            hashed_password=user.hashed_password,  
            owned_groups_list=json.dumps(user.owned_groups_list),
            joined_groups_list=json.dumps(user.joined_groups_list),
            pending_group_list=json.dumps(user.pending_group_list),
        )

        # I might need this. It is very unclear
        # # Insert statement using SQL Expression Language
        # stmt = insert(user_model.User).values(
        #     username=db_user.username,
        #     email=db_user.email,
        #     phone_number=db_user.phone_number,
        #     disabled=db_user.disabled,
        #     hashed_password=db_user.hashed_password,
        #     owned_groups_list=db_user.owned_groups_list,
        #     joined_groups_list=db_user.joined_groups_list,
        #     pending_group_list=db_user.pending_group_list
        # )

        # # Execute the insert operation
        # await db.execute(stmt)
        db.add(db_user)
        await db.commit()  # Commit the transaction
        await db.refresh(db_user)

        return db_user

    async def create_users(self, db: AsyncSession, users: list[user_schema.UserDB]) -> list[user_model.User]:
        db_users: list[user_model.User] = []
        for user in users:
            db_user = await self.create_user(db, user)
            db_users.append(db_user)
        return db_users

    async def get_user_by_username(self, db: AsyncSession, username: str) -> user_model.User | None:
        # Use 'select' instead of 'query'
        stmt = select(user_model.User).filter(user_model.User.username == username)
        result = await db.execute(stmt)
        
        # Fetch the first result, or return None if not found
        return result.scalars().first()

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> user_model.User | None:
        # Use 'select' instead of 'query'
        stmt = select(user_model.User).filter(user_model.User.id == user_id)
        result = await db.execute(stmt)
        
        # Fetch the first result, or return None if not found
        return result.scalars().first()

    def __user_to_schema__(self, db_user: user_model.User) -> user_schema.UserDB:
        return user_schema.UserDB(
            username=db_user.username,
            email=db_user.email,
            phone_number=db_user.phone_number,
            disabled=db_user.disabled,
            hashed_password=db_user.hashed_password,
            owned_groups_list=json.loads(db_user.owned_groups_list or "[]"),
            joined_groups_list=json.loads(db_user.joined_groups_list or "[]"),
            pending_group_list=json.loads(db_user.pending_group_list or "[]"),
        )