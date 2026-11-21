"""FastAPI application entrypoint."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import select
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.common import HealthResponse
from app.api import public, admin
from app.db.base import Base
from app.db.session import engine, AsyncSessionLocal
from app.models import AdminUser

logging.basicConfig(level=logging.DEBUG if settings.APP_DEBUG else logging.INFO)
logger = logging.getLogger("smart-assistant")
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. إنشاء الجداول
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 2. إنشاء حساب المسؤول الافتراضي
    logger.info("Checking default admin...")
    async with AsyncSessionLocal() as session:
        existing = await session.scalar(select(AdminUser).where(AdminUser.email == settings.ADMIN_INITIAL_EMAIL))
        if not existing:
            admin_user = AdminUser(
                email=settings.ADMIN_INITIAL_EMAIL,
                password_hash=pwd_ctx.hash(settings.ADMIN_INITIAL_PASSWORD),
                is_active=True
            )
            session.add(admin_user)
            await session.commit()
            logger.info("Default admin created.")
    
    yield

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, version="0.1.0", docs_url="/docs", lifespan=lifespan)
    
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
