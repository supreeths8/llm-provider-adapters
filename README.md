# llm-provider-adapters

A small Python tool for sending prompts to chat models. You can switch between model providers without changing any code.

It works with two providers:

- **Ollama** runs models on your own machine (default `qwen2.5:14b`). No API key needed.
- **OpenRouter** runs models in the cloud. You need an API key.

Each call gives you back the reply, the name of the model that answered, how many tokens were used (including cached ones), and how long it took.

## Setup

You need Python 3.12 or newer and [uv](https://docs.astral.sh/uv/). To use local models, install [Ollama](https://ollama.com) and download the model named in your `.env`.

```sh
cp .env.example .env   # then add your OpenRouter key
uv sync
uv run pre-commit install
```

Settings live in `.env`. Each one is named `PROVIDER__SETTING`, for example `OPENROUTER__API_KEY` or `OLLAMA__DEFAULT_MODEL`. Git ignores `.env`, so your key stays on your machine. The code also hides the key if settings are ever printed.

## Try it

```sh
uv run llm-provider-adapters ping                                   # local model through Ollama
uv run llm-provider-adapters ping --provider openrouter             # cloud model through OpenRouter
uv run llm-provider-adapters ping --prompt "Name three primes" --model <model-id>
```

You get the reply, then a line like `model · in 12 (cached 0) · out 8 · 0.42s`.

## How the code is organised

The main code only knows about one interface, `ChatModel`. The code that talks to each provider sits behind it, so you can swap providers without touching anything else.

```
src/llm_provider_adapters/
├── cli.py                    # Command line tool (the ping command)
├── config.py                 # Reads settings from .env
├── bootstrap.py              # Builds the right chat model for a provider
└── llm/
    ├── ports.py              # The ChatModel interface
    ├── models.py             # Request and response types
    ├── errors.py             # Error types
    └── openai_compatible.py  # Talks to any provider that uses the OpenAI API format
```

A few things to know:

- **One class covers both providers.** Ollama and OpenRouter both use the OpenAI API format, so the same class handles both. Only the settings change. A provider with a different API would get its own new class.
- **Clear errors.** You only ever see this project's own errors: the provider can't be reached, the provider sent back something unusable, or the API key is missing.
- **Safe with bad responses.** If a provider sends back no reply or no token counts, you get a clear error instead of a crash.

## Development

```sh
uv run pytest                # fast tests, no network
uv run pytest --integration  # also run tests that call a real model (Ollama must be running)
uv run ruff format && uv run ruff check --fix
uv run mypy
```

The fast tests use fake network responses, so they never call a real provider. A check runs before each commit: formatting, linting, type checks and the fast tests.
