from app.src.controller import user_controller
from app.src.models import schema as user_schema
from sqlalchemy.exc import IntegrityError
import pytest


def test_create_user(db, sample_user):
    created = user_controller.create_user(db, sample_user)
    assert created.username == sample_user.username
    assert created.email == sample_user.email
    assert created.phone_number == sample_user.phone_number


def test_get_user_by_username(db, sample_user):
    # Setup
    user_controller.create_user(db, sample_user)

    # Act
    fetched = user_controller.get_user_by_username(db, sample_user.username)

    # Assert
    assert fetched is not None
    assert fetched.username == sample_user.username


def test_get_user_by_username_returns_none_when_not_found(db):
    fetched = user_controller.get_user_by_username(db, "nonexistent")
    assert fetched is None


def test_create_user_duplicate_username_raises(db, sample_user):
    user_controller.create_user(db, sample_user)
    with pytest.raises(IntegrityError):
        user_controller.create_user(db, sample_user)
