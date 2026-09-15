from openai import OpenAI

from llm_provider_adapters.config import Provider, Settings
from llm_provider_adapters.llm.errors import MissingApiKeyError
from llm_provider_adapters.llm.openai_compatible import OpenAICompatibleChatModel
from llm_provider_adapters.llm.ports import ChatModel

# Ollama ignores the key, but the OpenAI client refuses to start without one.
_UNUSED_API_KEY = "not-needed"


def build_chat_model(provider: Provider, settings: Settings) -> ChatModel:
    provider_settings = settings.for_provider(provider)
    api_key = provider_settings.api_key.get_secret_value() if provider_settings.api_key else ""
    if provider_settings.requires_api_key and not api_key:
        raise MissingApiKeyError(provider.value)
    client = OpenAI(base_url=provider_settings.base_url, api_key=api_key or _UNUSED_API_KEY)
    return OpenAICompatibleChatModel(client, default_model=provider_settings.default_model)
