"""Create DB tables and the initial admin user."""
import asyncio
import sys
from passlib.context import CryptContext
from sqlalchemy import select
from app.core.config import settings
from app.db.base import Base
from app.db.session import AsyncSessionLocal, engine
from app.models import AdminUser

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def _ensure_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def _ensure_admin() -> None:
    async with AsyncSessionLocal() as session:
        existing = await session.scalar(select(AdminUser).where(AdminUser.email == settings.ADMIN_INITIAL_EMAIL))
        if existing:
            print(f"Admin already exists: {settings.ADMIN_INITIAL_EMAIL}")
            return
        admin = AdminUser(email=settings.ADMIN_INITIAL_EMAIL, password_hash=pwd_ctx.hash(settings.ADMIN_INITIAL_PASSWORD), is_active=True)
        session.add(admin)
        await session.commit()
        print(f"Created admin: {settings.ADMIN_INITIAL_EMAIL}")

async def main() -> None:
    await _ensure_tables()
    await _ensure_admin()
    await engine.dispose()
    print("Database initialized successfully.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        sys.exit(1)
