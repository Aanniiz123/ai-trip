from groq import AsyncGroq
from src.config import setting


class ChatService:
    def __init__(self):
        self.client = AsyncGroq(
            api_key=setting.CHAT_API
        )

    async def chat(self, message: str):
        response = await self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an intelligent AI travel assistant. "
                        "Help users suggesting destination, "
                        "recommend hotels, transportation, and activities."
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            temperature=0.7,
            max_tokens=100,
        )

        return response.choices[0].message.content