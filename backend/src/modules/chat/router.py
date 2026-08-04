from fastapi import APIRouter, HTTPException
from src.modules.chat.schemas import ChatRequest, ChatResponse
from src.modules.chat.service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

chat_service = ChatService()


@router.get("/status")
async def status():
    return {
        "status": "ok",
        "message": "Chat service is running."
    }


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):

    try:
        reply = await chat_service.chat(request.message)

        return ChatResponse(
            response=reply
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )