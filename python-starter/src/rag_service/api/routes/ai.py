from dataclasses import asdict

from fastapi import APIRouter, Depends

from rag_service.api.dependencies import get_npc_dialogue_service
from rag_service.api.schemas import AiCapabilitiesResponse, NpcTurnRequest, NpcTurnResponse
from rag_service.application.services.npc_dialogue import NpcDialogueService
from rag_service.config.settings import get_settings

router = APIRouter(prefix="/v1/ai", tags=["game-ai"])


@router.get("/capabilities", response_model=AiCapabilitiesResponse)
def capabilities() -> AiCapabilitiesResponse:
    settings = get_settings()
    return AiCapabilitiesResponse(
        embedding_provider=settings.embedding_provider,
        embedding_model=settings.embedding_model,
        vector_store_provider=settings.vector_store_provider,
        npc_provider=settings.npc_provider,
        npc_model=settings.huggingface_chat_model if settings.npc_provider == "huggingface" else "local",
        huggingface_token_configured=settings.huggingface_token is not None,
    )


@router.post("/npc/turn", response_model=NpcTurnResponse)
def npc_turn(
    request: NpcTurnRequest,
    service: NpcDialogueService = Depends(get_npc_dialogue_service),
) -> NpcTurnResponse:
    reply = service.reply(request.character, request.player_message, request.state, request.top_k)
    return NpcTurnResponse(**asdict(reply))
