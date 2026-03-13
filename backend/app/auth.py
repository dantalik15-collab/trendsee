from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_expire_minutes
    )
    payload = {
        "sub": str(user_id),
        "exp": expire,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> int | None:
    """Декодирует JWT и возвращает user_id или None при невалидном токене."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id_raw = payload.get("sub")
        if user_id_raw is None:
            return None
        return int(user_id_raw)
    except (jwt.InvalidTokenError, ValueError):
        return None
