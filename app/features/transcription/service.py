from app.interfaces.transcription import ITranscriptionProvider

class TranscriptService:
    def __init__(self, provider: ITranscriptionProvider):
        self.provider = provider


    async def from_youtube_url(self, url: str, lang_hint: str | None) -> str:
        return await self.provider.from_youtube_url(url, lang_hint=lang_hint)