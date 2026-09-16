from typing import Annotated

import typer
from rich.console import Console

from llm_provider_adapters.bootstrap import build_chat_model
from llm_provider_adapters.config import Provider, Settings
from llm_provider_adapters.llm.errors import LLMError
from llm_provider_adapters.llm.models import ChatRequest, Message, Role

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.callback()
def main() -> None:
    """AI sprint project."""


@app.command()
def ping(
    provider: Annotated[Provider, typer.Option(help="Which provider to call.")] = Provider.OLLAMA,
    prompt: Annotated[str, typer.Option(help="Prompt to send.")] = "Say hello in five words.",
    model: Annotated[str | None, typer.Option(help="Override the provider's default model.")] = None,
) -> None:
    """Send one prompt and print the reply, token usage and latency."""
    try:
        chat_model = build_chat_model(provider, Settings())
        response = chat_model.complete(ChatRequest(messages=(Message(role=Role.USER, content=prompt),), model=model))
    except LLMError as error:
        console.print(f"[red]{type(error).__name__}:[/red] {error}")
        raise typer.Exit(code=1) from error
    console.print(response.text)
    usage = response.usage
    console.print(
        f"[dim]{response.model} · in {usage.input_tokens} (cached {usage.cached_input_tokens})"
        f" · out {usage.output_tokens} · {response.latency_seconds:.2f}s[/dim]"
    )
