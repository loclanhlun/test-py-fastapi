from pydantic import BaseModel

class ImageGenRequest(BaseModel):
    prompt: str
    size: str = "1024x1024"

class ImageGenResponse(BaseModel):
    file_url: str