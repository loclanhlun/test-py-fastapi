from fastapi import APIRouter, Depends

from .schemas import RewriteRequest, RewriteResponse
from .service import RewriteService
from app.container import get_rewrite_service

router = APIRouter(prefix="/rewrite", tags=["rewrite"])


@router.post("", response_model=RewriteResponse)
async def rewrite(req: RewriteRequest, svc: RewriteService = Depends(get_rewrite_service)):
    out = await svc.rewrite(req.content, req.style, req.level)
    return RewriteResponse(content=out)