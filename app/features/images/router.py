from fastapi import APIRouter, Depends

from .schemas import ImageGenRequest, ImageGenResponse
from .service import ImageGenService
from app.container import get_image_gen_service

router = APIRouter(prefix="/images", tags=["images"])


@router.post("", response_model=ImageGenResponse)
async def create_image(req: ImageGenRequest, svc: ImageGenService = Depends(get_image_gen_service)):
    url = await svc.generate(req.prompt, req.size)
    return ImageGenResponse(file_url=url)