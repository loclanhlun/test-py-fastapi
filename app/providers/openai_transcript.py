from openai import OpenAI
import tempfile, os, glob
import anyio
from yt_dlp import YoutubeDL

ACCEPTED_AUDIO_EXTS = (".m4a", ".mp3", ".mp4", ".mpeg", ".mpga", ".wav", ".webm", ".ogg", ".flac", ".opus")
class OpenAIWhiser:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    

    async def from_youtube_url(self, url: str, *, lang_hint: str | None = None) -> str:
        from app.shared.transcripts import get_youtube_captions
        text = get_youtube_captions(url=url)
        if text:
            return text
        
        with tempfile.TemporaryDirectory() as td:
            audio_path = os.path.join(td, "audio.m4a")
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": audio_path,
                "quiet": True,
                "noplaylist": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                    "preferredquality": "192"
                }]
            }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        candidates = []
        for ext in ACCEPTED_AUDIO_EXTS:
            candidates.extend(glob.glob(os.path.join(td, f"*{ext}")))
        if not candidates:
            raise RuntimeError("Audio download succeeded but no supported audio file was found.")

        audio_path = candidates[0]
        
        def _call():
            with open(audio_path, "rb") as f:
                return self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    language=lang_hint
                )
            
        response = await anyio.to_thread.run_sync(_call)

        return response.text.strip()