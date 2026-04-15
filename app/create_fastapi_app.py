from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.models import db_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()

def create_app() -> FastAPI:
    app = FastAPI(Title="License System API", lifespan=lifespan)
    return app