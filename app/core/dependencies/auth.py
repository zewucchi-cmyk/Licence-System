from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from core.auth.fastapi_users import current_active_user
from core.models import User


async def superuser_required(user: User = Depends(current_active_user)):
    if not user.is_superuser:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Superuser privileges required"
        )
    return user
