import asyncio

from app.services.ollama import OllamaService
from app.services.serpapi import SerpApiService


class MockSerpApiClient:
    requested_params = {}

    def __init__(self, **kwargs):
        pass

    def search(self, params):
        type(self).requested_params = params
        return {"organic_results": [{"title": "Example"}]}


def test_serpapi_search_uses_configured_key_and_engine(monkeypatch):
    monkeypatch.setattr("app.services.serpapi.serpapi.Client", MockSerpApiClient)
    service = SerpApiService("test-key")

    payload = asyncio.run(service.search("example query", engine="google_shopping"))

    assert payload["organic_results"][0]["title"] == "Example"
    assert MockSerpApiClient.requested_params["engine"] == "google_shopping"
    assert "api_key" not in MockSerpApiClient.requested_params


def test_ollama_lists_local_models(monkeypatch):
    class MockAsyncClient:
        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def get(self, url):
            class Response:
                def raise_for_status(self):
                    return None

                def json(self):
                    return {"models": [{"name": "qwen3:4b"}]}

            return Response()

    monkeypatch.setattr("app.services.ollama.httpx.AsyncClient", MockAsyncClient)
    service = OllamaService("http://localhost:11434", "qwen3:4b")

    assert asyncio.run(service.health()) == (True, True)
