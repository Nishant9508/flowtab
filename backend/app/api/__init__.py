from fastapi import APIRouter
from .demo import router as demo_router
from .network import router as network_router

api_router = APIRouter()
api_router.include_router(demo_router, prefix="/demo", tags=["demo"])
api_router.include_router(network_router, prefix="/network")
