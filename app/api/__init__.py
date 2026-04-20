from fastapi import APIRouter

from core.config import settings
from .licences.views import router as licences_router
from .products.views import router as products_router

router = APIRouter(prefix=settings.api.prefix)

router.include_router(licences_router, prefix=settings.api.version + settings.api.licences.endpoint)
router.include_router(products_router, prefix=settings.api.version + settings.api.products.endpoint)