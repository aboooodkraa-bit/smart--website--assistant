from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.schemas.common import ORMModel

class MessageResponse(ORMModel):
    id: int
    role: str
    content: str
    source: str
    created_at: datetime

class ConversationCreate(BaseModel):
    language: str = "ar"

class ConversationResponse(ORMModel):
    id: str
    session_token: str
    language: str
    created_at: datetime
    messages: List[MessageResponse] = []
