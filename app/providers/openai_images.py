import anyio.to_thread
from openai import OpenAI
import base64
import anyio
import logging

class OpenAIImagegen:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    async def generate(self, prompt: str, *, size: str = "1024x1024") -> bytes:
        def _call():
            return self.client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                n=1,
                size=size
            )
        response = await anyio.to_thread.run_sync(_call)
        logging.info(response)

        return base64.b64decode(response.data[0].b64_json)