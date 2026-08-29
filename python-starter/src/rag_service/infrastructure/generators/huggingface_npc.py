import json
from collections.abc import Sequence
from typing import Any, Protocol

from rag_service.domain.entities import Chunk, NpcAction, NpcReply


class ChatClient(Protocol):
    def chat_completion(self, *, messages: list[dict[str, str]], **kwargs: Any) -> Any: ...


class HuggingFaceNpcGenerator:
    def __init__(
        self,
        model: str,
        token: str,
        provider: str = "auto",
        max_tokens: int = 300,
        client: ChatClient | None = None,
    ) -> None:
        self.model = model
        self._max_tokens = max_tokens
        if client is None:
            from huggingface_hub import InferenceClient

            client = InferenceClient(model=model, token=token, provider=provider)
        self._client = client

    def reply(
        self,
        character: str,
        player_message: str,
        state: dict[str, str],
        context: Sequence[Chunk],
    ) -> NpcReply:
        lore = "\n".join(chunk.content for chunk in context) or "No relevant lore was retrieved."
        system = (
            "You are an NPC dialogue engine. Stay in character and ground every factual claim in the supplied lore. "
            "Return JSON only with keys speech, emotion, intent, and actions. actions is an array of objects with "
            "kind, target, and value. Never change authoritative game state; only propose actions."
        )
        user = json.dumps(
            {"character": character, "player_message": player_message, "state": state, "lore": lore},
            ensure_ascii=False,
        )
        response = self._client.chat_completion(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=self._max_tokens,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        payload = self._parse_json(content)
        actions = tuple(
            NpcAction(str(item["kind"]), item.get("target"), item.get("value"))
            for item in payload.get("actions", [])
            if isinstance(item, dict) and item.get("kind")
        )
        speech = str(payload.get("speech", "")).strip()
        if not speech:
            raise ValueError("Hugging Face NPC response did not contain speech")
        return NpcReply(speech, str(payload.get("emotion", "neutral")), str(payload.get("intent", "conversation")), actions)

    @staticmethod
    def _parse_json(content: str) -> dict[str, Any]:
        text = content.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        payload = json.loads(text)
        if not isinstance(payload, dict):
            raise ValueError("Hugging Face NPC response must be a JSON object")
        return payload
