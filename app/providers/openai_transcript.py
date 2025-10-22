import openai
import tempfile
import os
import glob
from yt_dlp import YoutubeDL
import anyio

ACCEPTED_AUDIO_EXTS = (".m4a", ".mp3", ".mp4", ".mpeg", ".mpga", ".wav", ".webm", ".ogg", ".flac", ".opus")

class OpenAIWhisper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    async def from_youtube_url(self, url: str, *, lang_hint: str | None = None, model_option: str) -> str:
        from app.shared.transcripts import get_youtube_captions

        if model_option == "default":
            transcript = get_youtube_captions(url=url)
        elif model_option == "chat_gpt":
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

                try:
                    with YoutubeDL(ydl_opts) as ydl:
                        ydl.extract_info(url, download=True)
                except Exception as e:
                    raise RuntimeError(f"Failed to download audio: {e}")

                candidates = []
                for ext in ACCEPTED_AUDIO_EXTS:
                    candidates.extend(glob.glob(os.path.join(td, f"*{ext}")))
                if not candidates:
                    raise RuntimeError("Audio download succeeded but no supported audio file was found.")

                audio_path = candidates[0]

                def _call():
                    with open(audio_path, "rb") as f:
                        return openai.Audio.transcribe(
                            model="whisper-1",
                            file=f,
                            language=lang_hint
                        )

                try:
                    response = await anyio.to_thread.run_sync(_call)
                    transcript = response["text"].strip()
                except Exception as e:
                    raise RuntimeError(f"Failed to transcribe audio: {e}")
        else:
            raise ValueError(f"Unsupported model_option: {model_option}")

        return transcript
