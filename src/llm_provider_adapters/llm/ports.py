from typing import Protocol

from llm_provider_adapters.llm.models import ChatRequest, ChatResponse


class ChatModel(Protocol):
    def complete(self, request: ChatRequest) -> ChatResponse:
        """Send one chat request and return the reply with usage and latency.

        Raises an `LLMError` subclass on failure, never a provider-specific exception.
        """
        ...
