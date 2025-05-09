import pytest
from jose import jwt
from datetime import timedelta
from fastapi import HTTPException

from app.src.util.auth import create_access_token, decode_token, hash_password, verify_password, get_current_user, SECRET_KEY, ALGORITHM

# Passwords
def test_hash_and_verify_password():
    password = "secure_password_123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)

def test_hash_and_verify_password_battery(sample_passwords):
    for password in sample_passwords:
        hashed = hash_password(password)

        assert hashed != password
        assert verify_password(password, hashed)

def test_create_and_decode_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data.copy(), expires_delta=timedelta(minutes=5))
    
    decoded = decode_token(token)
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded


@pytest.mark.asyncio
async def test_get_current_user_valid_token(db, sample_raw_user):

    db.add(sample_raw_user)
    await db.commit()

    token = jwt.encode({"sub": sample_raw_user.username}, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token, db=db)

    assert user.username == sample_raw_user.username

@pytest.mark.asyncio
async def test_get_current_user_invalid_token_raises(db, sample_raw_user):

    db.add(sample_raw_user)
    await db.commit()

    invalid_token = "not.a.real.token"

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=invalid_token, db=db)

    assert exc_info.value.status_code == 401