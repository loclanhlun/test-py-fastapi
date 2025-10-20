import httpx

class OpenAIChatRewriter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base = "https://api.openai.com/v1"
    async def rewrite(self, text: str, *, style: str | None = None, level: str | None = None) -> str:
        prompt = "Rewrite the content with clarity and coherence"
        if style: prompt += f", style: {style}"
        if level: prompt += f", level: {level}"
        prompt += f".\n\nContent:\n{text}"

        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                f"{self.base}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                }
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()