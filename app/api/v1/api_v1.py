from fastapi import APIRouter
from app.api.v1.endpoints.au import test


router = APIRouter()

# Include version 1 endpoints
router.include_router(test.router, prefix="/test", tags=["test"])

