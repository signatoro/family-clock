
from sqlalchemy.orm import Session
from app.src.models import user as user_model
from app.src.models import schema as user_schema
import json
import bcrypt


def create_user(db: Session, user: user_schema.UserDB) -> user_model.User:
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
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_users(db: Session, users: list[user_schema.UserDB]) -> list[user_model.User]:
    db_users: list[user_model.User] = []
    for user in users:
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
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db_users.append(db_user)
    return db_users


def get_user_by_username(db: Session, username: str) -> user_model.User | None:
    return db.query(user_model.User).filter(user_model.User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> user_model.User | None:
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def __user_to_schema__(db_user: user_model.User) -> user_schema.UserDB:
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