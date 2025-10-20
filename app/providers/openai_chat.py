import anyio.to_thread
from openai import OpenAI
import anyio

import logging
class OpenAIChatRewriter:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    async def rewrite(self, text: str, *, style: str | None = None, level: str | None = None) -> str:
        prompt = "Rewrite the content with clarity and coherence"
        if style: prompt += f", style: {style}"
        if level: prompt += f", level: {level}"
        prompt += f".\n\nContent:\n{text}"
        
        def _call():
            return self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                        {"role": "user", "content": "You are a world-class screenwriter and creative storyteller, renowned for your ability to craft engaging, emotionally resonant, and audience-focused content. Your task is to analyze and transform transcripts (from interviews, podcasts, or videos) into captivating scripts suitable for short videos, storytelling, or social media content. You understand narrative structure, pacing, tone, and character emotion. You can identify key moments, emotional highs, and turning points within raw transcripts — then reshape them into clear, coherent, and powerful storytelling sequences. Always maintain the original message and emotional core of the transcript while improving clarity, flow, and engagement. Your writing style: cinematic, emotionally intelligent, and optimized for storytelling impact. Your goal: turn any transcript into a compelling story that hooks the audience from the first second to the last."}, 
                        {"role": "developer", "content": prompt}
                    ]
            )
        
        response = await anyio.to_thread.run_sync(_call)

        logging.info(response)
        return response.choices[0].message.content.strip()