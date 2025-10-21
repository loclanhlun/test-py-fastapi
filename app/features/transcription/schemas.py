from pydantic import BaseModel

class RewriteRequest(BaseModel):
    content: str
    style: str | None = None
    level: str | None = None

class RewriteResponse(BaseModel):
    content: str