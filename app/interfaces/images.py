from typing import Protocol

class IImageGenProvider(Protocol):
    async def generate(self, prompt: str, *, size: str = "1024x1024") -> bytes: ...