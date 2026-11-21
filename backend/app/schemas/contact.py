from pydantic import BaseModel, Field
from typing import Optional

class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    contact_method: str = Field(..., pattern="^(email|phone|telegram|whatsapp)$")
    contact_value: str = Field(..., min_length=3, max_length=200)
    message: Optional[str] = None
    consent_given: bool = Field(..., description="User must consent to data processing")
    conversation_id: Optional[str] = None
