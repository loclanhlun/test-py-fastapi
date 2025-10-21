from typing import Optional, List
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import re, logging

def extract_youtube_id(url: str) -> Optional[str]:
    m = re.search(r"(?:v=|/shorts/|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    
    return m.group(1) if m else None

def get_youtube_captions(url: str, lang_priority: List[str] = ["en", "vi"]) -> Optional[str]:
    vid = extract_youtube_id(url)
    ydl = YouTubeTranscriptApi()
    if not vid:
        return None
    try:
        for lang in lang_priority:
            try:
                segs_raw_data = ydl.fetch(video_id=vid, languages=[lang]).to_raw_data()
                transcripts = " ".join(item['text'] for item in segs_raw_data if item["text"].strip())
                return transcripts
        
            except NoTranscriptFound:
                logging.info("NoTranscriptFound")
                continue
        
    except (NoTranscriptFound, TranscriptsDisabled):
        return None
    except Exception:
        return None
    return None