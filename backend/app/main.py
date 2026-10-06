from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import get_settings
from app.services.ollama import OllamaError, OllamaService
from app.services.serpapi import SerpApiService

settings = get_settings()
serpapi = SerpApiService(settings.serpapi_api_key, settings.request_timeout_seconds)
ollama = OllamaService(settings.ollama_base_url, settings.ollama_model, settings.request_timeout_seconds)


class HealthResponse(BaseModel):
    status: str
    service: str


class DependencyHealth(BaseModel):
    configured: bool
    available: bool | None = None
    model: str | None = None
    message: str | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="trustlens-api")


@app.get("/api/health/serpapi", response_model=DependencyHealth)
async def serpapi_health() -> DependencyHealth:
    configured = serpapi.configured
    return DependencyHealth(
        configured=configured,
        available=None,
        message="API key configured; no billable search was made." if configured else "Set SERPAPI_API_KEY to enable searches.",
    )


@app.get("/api/health/ollama", response_model=DependencyHealth)
async def ollama_health() -> DependencyHealth:
    try:
        _, model_available = await ollama.health()
        message = None if model_available else f"Ollama is running, but {settings.ollama_model} is not installed."
        return DependencyHealth(configured=True, available=model_available, model=settings.ollama_model, message=message)
    except OllamaError as exc:
        return DependencyHealth(configured=True, available=False, model=settings.ollama_model, message=str(exc))
