from pydantic import BaseModel, HttpUrl

class TranscriptRequest(BaseModel):
    url: HttpUrl
    lang_hint: str | None = None

class TranscriptResponse(BaseModel):
    text: str