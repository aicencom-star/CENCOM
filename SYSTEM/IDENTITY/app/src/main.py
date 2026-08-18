from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from pydantic import BaseModel

from app.src.database import SessionLocal
from app.src.crud import authenticate_user
from app.src.jwt_handler import (
    create_access_token,
    decode_access_token,
)


app = FastAPI(
    title="CENCOM IDENTITY",
    description="Hệ thống xác thực và quản lý danh tính CENCOM",
    version="1.0.0",
)


# ============================================================
# OAUTH2
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ============================================================
# RESPONSE MODEL
# ============================================================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class CurrentUserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: str | None
    is_active: bool


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "system": "CENCOM IDENTITY",
        "status": "running",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "identity",
    }


# ============================================================
# DATABASE HEALTH
# ============================================================

@app.get("/health/database")
def health_database():

    db = SessionLocal()

    try:

        db.execute("SELECT 1")

        return {
            "status": "ok",
            "database": "CENCOM_IDENTITY",
        }

    except Exception as e:

        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {str(e)}",
        )

    finally:

        db.close()


# ============================================================
# LOGIN
# ============================================================

@app.post(
    "/auth/login",
    response_model=TokenResponse,
)
def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends()
    ],
):

    db = SessionLocal()

    try:

        user = authenticate_user(
            db,
            form_data.username,
            form_data.password,
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        if not user.is_active:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        access_token = create_access_token(
            user_id=user.id,
            username=user.username,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    finally:

        db.close()


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):

    payload = decode_access_token(token)

    if not payload:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    user_id = payload.get("sub")

    if not user_id:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    db = SessionLocal()

    try:

        from app.src.models import User

        user = (
            db.query(User)
            .filter(User.id == int(user_id))
            .first()
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        if not user.is_active:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        return user

    finally:

        db.close()


# ============================================================
# CURRENT USER API
# ============================================================

@app.get(
    "/auth/me",
    response_model=CurrentUserResponse,
)
def auth_me(
    current_user = Depends(get_current_user),
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "is_active": current_user.is_active,
    }