from typing import Any

import httpx


class OllamaError(RuntimeError):
    """Raised when the configured local Ollama service is unavailable."""


class OllamaService:
    def __init__(self, base_url: str, model: str, timeout: float = 8.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    async def list_models(self) -> list[str]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                payload: Any = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise OllamaError("Ollama is unavailable. Start Ollama and check OLLAMA_BASE_URL.") from exc

        models = payload.get("models", []) if isinstance(payload, dict) else []
        return [item["name"] for item in models if isinstance(item, dict) and isinstance(item.get("name"), str)]

    async def health(self) -> tuple[bool, bool]:
        models = await self.list_models()
        available = self.model in models or f"{self.model}:latest" in models
        return True, available
