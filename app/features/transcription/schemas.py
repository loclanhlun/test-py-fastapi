from pydantic import BaseModel, HttpUrl

class TranscriptRequest(BaseModel):
    url: HttpUrl
    lang_hint: str | None = None
    model_option: str

class TranscriptResponse(BaseModel):
    transcripts: str | None = None