from typing import Optional, List, Dict
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

import re

def extract_youtube_id(url: str) -> Optional[str]:
    m = re.search(r"(?:v=|/shorts/|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else None

def get_youtube_captions(url: str, lang_priority: List[str] = ["en", "vi"]) -> Optional[str]:
    vid = extract_youtube_id(url)
    if not vid:
        return None
    
    try:
        for lang in lang_priority:
            try:
                segs = YouTubeTranscriptApi.fetch(video_id=vid, languages=[lang])
                return " ".join(s["text"] for s in segs if s["text"].strip())
            except NoTranscriptFound:
                continue

        transcript_list = YouTubeTranscriptApi.list(video_id=vid)
        transcript = transcript_list.find_transcript(["en","vi"])
        if not transcript:
            transcript = transcript_list.find_generated_transcript(["en", "vi"])
        
        return " ".join(s["text"] for s in transcript if s["text"].strip())
        
    except (NoTranscriptFound, TranscriptsDisabled):
        return None
    except Exception:
        return None
    return None