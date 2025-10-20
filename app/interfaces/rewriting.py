from typing import Protocol

class IRewriteProvider(Protocol):
    async def rewrite(self, text: str, *, style: str | None = None, level: str | None = None) -> str: ...