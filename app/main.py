from create_fastapi_app import create_app

main_app = create_app()

@main_app.get("/")
async def root():
    return {"message": "running"}

@main_app.get("/health")
async def health():
    return {"message": "healthy"}