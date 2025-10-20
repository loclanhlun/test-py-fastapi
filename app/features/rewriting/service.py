from app.interfaces.rewriting import IRewriteProvider

class RewriteService:
    def __init__(self, provider: IRewriteProvider):
        self.provider = provider


    async def rewrite(self, content: str, style: str | None, level: str | None) -> str:
        return await self.provider.rewrite(content, style=style, level=level)