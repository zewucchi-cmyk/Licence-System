import os
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from core.config import settings

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy():
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=3600,
    )

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)