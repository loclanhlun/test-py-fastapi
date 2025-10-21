from fastapi import APIRouter, Depends

from .schemas import TranscriptRequest, TranscriptResponse
from .service import TranscriptService
from app.container import get_transcription_service

router = APIRouter(prefix="/transcription", tags=["transcription"])


@router.post("", response_model=TranscriptResponse)
async def transcript_from_url(req: TranscriptRequest, svc: TranscriptService = Depends(get_transcription_service)):
    text = await svc.from_youtube_url(str(req.url), req.lang_hint)
    return TranscriptResponse(text=text)