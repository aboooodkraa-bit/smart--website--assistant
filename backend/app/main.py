"""FastAPI application entrypoint."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.schemas.common import HealthResponse
from app.api import public, admin

logging.basicConfig(level=logging.DEBUG if settings.APP_DEBUG else logging.INFO)
logger = logging.getLogger("smart-assistant")

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, version="0.1.0", docs_url="/docs")
    
    if settings.allowed_origins_list:
        app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    app.include_router(public.router, prefix="/api", tags=["public"])
    app.include_router(admin.router, prefix="/admin", tags=["admin"])

    @app.get("/health", response_model=HealthResponse, tags=["meta"])
    async def health() -> HealthResponse:
        return HealthResponse(status="ok", app=settings.APP_NAME, env=settings.APP_ENV, version="0.1.0")
        
    @app.get("/chatbot-widget.js", include_in_schema=False)
    async def serve_widget():
        return FileResponse("app/static/chatbot-widget.js")

    return app

app = create_app()
