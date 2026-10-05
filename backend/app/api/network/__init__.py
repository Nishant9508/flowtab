from fastapi import APIRouter
from .views import router as views_router
from .scopes import router as scopes_router

router = APIRouter()
router.include_router(views_router, tags=["network"])
router.include_router(scopes_router, prefix="/scopes", tags=["network"])
