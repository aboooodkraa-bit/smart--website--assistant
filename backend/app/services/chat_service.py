import json
from pathlib import Path
from typing import Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ai_service import AIService
from app.models.conversation import Conversation
from app.models.message import Message

class ChatService:
    def __init__(self):
        self.ai = AIService()
        self.knowledge_dir = Path("knowledge")

    def _load_knowledge(self, lang: str) -> str:
        file_path = self.knowledge_dir / f"website-info.{lang}.json"
        if not file_path.exists():
            return ""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return "\n".join([f"- {k}: {v}" for k, v in data.items()])

    async def process_message(self, db: AsyncSession, conversation_id: str, message: str, lang: str = "ar", source: str = "text") -> Dict:
        # جلب المحادثة أو إنشائها
        result = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
        conv = result.scalar_one_or_none()
        
        if not conv:
            conv = Conversation(id=conversation_id, language=lang)
            db.add(conv)
            await db.commit()

        # حفظ رسالة المستخدم
        user_msg = Message(conversation_id=conv.id, role="user", content=message, source=source)
        db.add(user_msg)

        # معالجة الرد
        if source == "quick_reply":
            reply = "شكراً لاختيارك هذا الخيار." if lang == "ar" else "Merci d'avoir choisi cette option."
            reply_source = "quick_reply"
        else:
            knowledge_context = self._load_knowledge(lang)
            reply = await self.ai.generate_reply(messages=[{"role": "user", "content": message}], knowledge_context=knowledge_context)
            reply_source = "ai"

        # حفظ رد المساعد
        bot_msg = Message(conversation_id=conv.id, role="assistant", content=reply, source=reply_source)
        db.add(bot_msg)
        await db.commit()

        return {"reply": reply, "source": reply_source}

chat_service = ChatService()
