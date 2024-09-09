from fastapi import APIRouter

from .auntification import router as auntification_router

__all__ = ["router"]

router = APIRouter()

router.include_router(auntification_router)
