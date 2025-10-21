from typing import Protocol

class ITranscriptionProvider(Protocol):
    async def from_youtube_url(self, url: str, *, lang_hint: str | None = None) -> str: ...