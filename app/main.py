import uvicorn

from create_fastapi_app import create_app

from api import router as api_router
from core.auth.fastapi_users import fastapi_users, auth_backend
from core.schemas.user import UserRead, UserCreate
main_app = create_app()

@main_app.get("/")
async def root():
    return {"message": "running"}

@main_app.get("/health")
async def health():
    return {"message": "healthy"}

main_app.include_router(api_router)

main_app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

main_app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["auth"],
)

if __name__ == '__main__':
    uvicorn.run(main_app, host="127.0.0.1", port=8080)
