import asyncio
from typing import Any

import serpapi


class SerpApiError(RuntimeError):
    """Raised when SerpApi cannot return a search response."""


class SerpApiService:
    """Async boundary around SerpApi's maintained Python SDK."""

    def __init__(self, api_key: str, timeout: float = 8.0) -> None:
        self.api_key = api_key
        self.timeout = timeout

    @property
    def configured(self) -> bool:
        return bool(self.api_key.strip())

    async def search(self, query: str, *, engine: str = "google", **options: Any) -> dict[str, Any]:
        if not self.configured:
            raise SerpApiError("SerpApi is not configured. Set SERPAPI_API_KEY.")

        params = {"engine": engine, "q": query, **options}
        try:
            client = serpapi.Client(api_key=self.api_key, timeout=self.timeout)
            payload = await asyncio.to_thread(client.search, params)
        except Exception as exc:
            raise SerpApiError("SerpApi search failed.") from exc

        if not isinstance(payload, dict):
            raise SerpApiError("SerpApi returned an invalid response.")
        if payload.get("error"):
            raise SerpApiError("SerpApi returned an error.")
        return payload
