from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.contact_request import ContactRequest

router = APIRouter()

@router.get("/contacts")
async def list_contacts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ContactRequest).order_by(ContactRequest.created_at.desc()))
    return result.scalars().all()
