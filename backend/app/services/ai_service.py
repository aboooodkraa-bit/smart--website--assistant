from typing import List, Dict
from app.core.config import settings

class AIService:
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self.api_key = settings.OPENAI_API_KEY

    async def generate_reply(self, messages: List[Dict[str, str]], knowledge_context: str) -> str:
        system_prompt = f"""أنت مساعد ذكي لموقع إلكتروني. أجب بناءً على هذه المعلومات فقط:
{knowledge_context}
إذا لم تجد الإجابة، اطلب من المستخدم التواصل مع المسؤول. أجب بنفس لغة المستخدم (عربي أو فرنسي)."""
        
        if self.provider == "openai" and self.api_key:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.api_key, base_url=settings.OPENAI_BASE_URL)
            try:
                response = await client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[{"role": "system", "content": system_prompt}] + messages,
                    max_tokens=settings.AI_MAX_TOKENS,
                    timeout=settings.AI_TIMEOUT_SECONDS
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي. (الخطأ: {str(e)})"
        
        # الوضع الوهمي (Mock) في حال عدم وجود مفتاح API
        return "مرحباً! أنا مساعد ذكي تجريبي. (لم يتم تفعيل الذكاء الاصطناعي الحقيقي بعد). يمكنك التواصل مع المسؤول."
