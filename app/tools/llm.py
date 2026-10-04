
"""The single wrapper for every model call.

complete(prompt_name, user_input, schema) sends the prompt file
app/prompts/<prompt_name>.md plus user_input to the model and returns
an object of the given schema. Nothing else in the project talks to OpenAI.
"""
import logging
import time
from pathlib import Path
from typing import TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

from app.config import settings

log = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

# Dollars per 1 million tokens: (input, output). Update when prices change.
PRICES = {
    "gpt-6.1-sol": (2.00, 10.00),
    "gpt-6-luna": (0.10, 0.50),
}

T = TypeVar("T", bound=BaseModel)

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    """Create the OpenAI client the first time it is needed."""
    global _client
    if _client is None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing from .env")
        _client = AsyncOpenAI(api_key=settings.openai_api_key, timeout=60)
    return _client


def _cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    price_in, price_out = PRICES.get(model, (0.0, 0.0))
    return (input_tokens * price_in + output_tokens * price_out) / 1_000_000


async def complete(
    prompt_name: str,
    user_input: str,
    schema: type[T],
    model: str | None = None,
) -> T:
    model = model or settings.model_fast
    instructions = (PROMPTS_DIR / f"{prompt_name}.md").read_text(encoding="utf-8")

    start = time.perf_counter()
    response = await _get_client().responses.parse(
        model=model,
        instructions=instructions,
        input=user_input,
        text_format=schema,
    )
    ms = int((time.perf_counter() - start) * 1000)

    usage = response.usage
    cost = _cost_usd(model, usage.input_tokens, usage.output_tokens)
    log.info(
        "llm prompt=%s model=%s in=%d out=%d cost=$%.5f ms=%d",
        prompt_name, model, usage.input_tokens, usage.output_tokens, cost, ms,
    )

    result = response.output_parsed
    if result is None:
        raise RuntimeError(f"Model returned nothing usable for prompt '{prompt_name}'")
    return result