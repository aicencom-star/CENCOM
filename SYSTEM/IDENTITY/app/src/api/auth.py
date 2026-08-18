from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.src.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class LoginRequest(BaseModel):

    username: str
    password: str


@router.post("/test-password")
def test_password():

    password = "CENCOM123"

    hashed = hash_password(password)

    return {
        "password": password,
        "hash": hashed,
        "verified": verify_password(
            password,
            hashed
        )
    }


@router.post("/test-token")
def test_token():

    token = create_access_token({
        "sub": "test_user",
        "role": "ADMIN"
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }