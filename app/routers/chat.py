from fastapi import APIRouter, Depends, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ollama_service import OllamaService, get_ollama_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Send a chat message",
    description="Sends a prompt to the configured local Ollama model and returns the generated text.",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid request"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Ollama unavailable"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Unexpected server error"},
    },
)
async def chat(
    request: ChatRequest,
    ollama_service: OllamaService = Depends(get_ollama_service),
) -> ChatResponse:
    response = await ollama_service.generate_response(request.message)
    return ChatResponse(response=response)
