import uvicorn

from create_fastapi_app import create_app

from api import router as api_router
main_app = create_app()

@main_app.get("/")
async def root():
    return {"message": "running"}

@main_app.get("/health")
async def health():
    return {"message": "healthy"}

main_app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(main_app, host="127.0.0.1", port=8080)
