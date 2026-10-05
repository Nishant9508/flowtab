from fastapi import APIRouter
from .views import router as views_router
from .scopes import router as scopes_router
from .alerts import router as alerts_router

router = APIRouter()
router.include_router(views_router, tags=["network"])
router.include_router(scopes_router, prefix="/scopes", tags=["network"])
router.include_router(alerts_router, prefix="/insights", tags=["network"])
