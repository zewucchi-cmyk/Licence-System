from fastapi import APIRouter

from core.config import settings
from .licences.views import router as licences_router

router = APIRouter(prefix=settings.api.prefix)

router.include_router(licences_router, prefix=settings.api.version + settings.api.licences)