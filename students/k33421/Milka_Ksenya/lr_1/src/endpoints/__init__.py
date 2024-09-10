from fastapi import APIRouter

from .auntification import router as auntification_router
from .user import router as user_router

__all__ = ["router"]

router = APIRouter()

router.include_router(auntification_router)
router.include_router(user_router)
