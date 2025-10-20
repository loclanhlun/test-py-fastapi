from fastapi import APIRouter
from app.features.rewriting.router import router as rewriting


api_v1 = APIRouter(prefix="/v1")

api_v1.include_router(rewriting)