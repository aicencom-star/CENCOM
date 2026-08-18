from datetime import datetime, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from config.security import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    access_token_expire_delta,
)


def create_access_token(
    user_id: int,
    username: str,
) -> str:

    expire = datetime.now(timezone.utc) + access_token_expire_delta()

    payload = {
        "sub": str(user_id),
        "username": username,
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict | None:

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        if payload.get("type") != "access":
            return None

        return payload

    except InvalidTokenError:
        return None