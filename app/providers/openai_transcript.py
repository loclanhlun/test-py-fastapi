from openai import OpenAI

class OpenAIWhiserProvider:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    

    # async def from_youtube_url(self, url: str, *, lang_hint: str | None = None) -> str:
    #     # TODO: get bytes audio youtube 
    #     audio_bytes = None;
    #     def _call():
    #         return self.client.images.generate(
    #             model="gpt-image-1",
    #             prompt=prompt,
    #             n=1,
    #             size=size
    #         )
    #     response = await anyio.to_thread.run_sync(_call)
    #     logging.info(response)

    #     return base64.b64decode(response.data[0].b64_json)