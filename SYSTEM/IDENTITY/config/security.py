from datetime import timedelta
import os


# ============================================================
# CENCOM IDENTITY SECURITY CONFIG
# ============================================================

JWT_ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Trong giai đoạn phát triển có thể dùng biến môi trường.
# Tuyệt đối không đưa SECRET KEY thật lên GitHub.
JWT_SECRET_KEY = os.getenv(
    "CENCOM_JWT_SECRET",
    "CHANGE_THIS_CENCOM_JWT_SECRET_BEFORE_PRODUCTION"
)


def access_token_expire_delta() -> timedelta:
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)