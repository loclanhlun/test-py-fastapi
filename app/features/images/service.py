from app.interfaces.images import IImageGenProvider
import uuid, os

class ImageGenService:
    def __init__(self, provider: IImageGenProvider, downloads_dir: str = "downloads"):
        self.provider = provider
        self.downloads_dir = downloads_dir
        os.makedirs(self.downloads_dir, exist_ok=True)


    async def generate(self, prompt: str, size: str = "1024x1024") -> bytes:
        img_bytes = await self.provider.generate(prompt=prompt,size=size)
        fname = f"{uuid.uuid4()}.png"
        path = os.path.join(self.downloads_dir, fname)
        with open(path, "wb") as f:
            f.write(img_bytes)
        return f"/downloads/{fname}"