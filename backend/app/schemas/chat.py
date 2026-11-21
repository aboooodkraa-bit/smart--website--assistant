from pydantic import BaseModel, Field
from typing import Optional, Dict, List

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    language: str = Field("ar", pattern="^(ar|fr)$")
    source: str = Field("text", pattern="^(text|quick_reply)$")
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    source: str
    suggestions: List[Dict[str, str]] = []
