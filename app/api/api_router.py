from fastapi import APIRouter
from app.api.v1.api_v1 import router as v1_router

# from app.api.v1.endpoints import auth

api_router = APIRouter()

api_router.include_router(v1_router, prefix="/v1")
# api_router.include_router(auth.router, prefix="/auth")
