from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.contact import ContactCreate
from app.services.chat_service import chat_service
from app.models.contact_request import ContactRequest
import json
from pathlib import Path
import uuid

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    conv_id = request.conversation_id or uuid.uuid4().hex
    result = await chat_service.process_message(
        db=db, conversation_id=conv_id, message=request.message, lang=request.language, source=request.source
    )
    
    qr_path = Path("knowledge/quick-replies.json")
    suggestions = []
    if qr_path.exists():
        with open(qr_path, "r", encoding="utf-8") as f:
            suggestions = json.load(f).get(request.language, [])

    return ChatResponse(reply=result["reply"], source=result["source"], suggestions=suggestions)

@router.post("/contact")
async def create_contact(request: ContactCreate, db: AsyncSession = Depends(get_db)):
    if not request.consent_given:
        return {"status": "error", "message": "Consent required."}
    
    contact = ContactRequest(
        name=request.name, contact_method=request.contact_method,
        contact_value=request.contact_value, message=request.message,
        consent_given=request.consent_given, conversation_id=request.conversation_id
    )
    db.add(contact)
    await db.commit()
    return {"status": "success", "message": "Contact request saved."}

@router.get("/config")
async def get_config():
    return {"app_name": "Smart Website Assistant", "default_language": "ar", "languages": ["ar", "fr"]}
