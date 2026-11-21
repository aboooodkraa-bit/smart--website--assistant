from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.contact_request import ContactRequest
    from app.models.message import Message

def _uuid() -> str:
    return uuid4().hex

class Conversation(Base, TimestampMixin):
    __tablename__ = "conversations"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    session_token: Mapped[str] = mapped_column(String(64), unique=True, index=True, default=lambda: uuid4().hex)
    language: Mapped[str] = mapped_column(String(5), default="ar")
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    messages: Mapped[list["Message"]] = relationship(back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")
    contact_requests: Mapped[list["ContactRequest"]] = relationship(back_populates="conversation", cascade="all, delete-orphan")
