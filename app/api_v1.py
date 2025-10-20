from fastapi import APIRouter
from app.features.rewriting.router import router as rewriting
from app.features.images.router import router as images


api_v1 = APIRouter(prefix="/v1")

api_v1.include_router(rewriting)
api_v1.include_router(images)