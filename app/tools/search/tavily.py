"""
STEP 2. Tavily provider over httpx. Maps HTTP errors to base error types.
"""
"""Tavily search: a question in, a list of SearchResult out."""
import logging
import time

import httpx

from app.config import settings
from app.tools.search.base import FatalError, RetryableError, SearchResult

log = logging.getLogger(__name__)

URL = "https://api.tavily.com/search"


async def search(query: str, max_results: int = 5) -> list[SearchResult]:
    if not settings.tavily_api_key:
        raise FatalError("TAVILY_API_KEY is missing from .env")

    start = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=settings.search_timeout_s) as client:
            response = await client.post(
                URL,
                headers={"Authorization": f"Bearer {settings.tavily_api_key}"},
                json={
                    "query": query,
                    "max_results": max_results,
                    "include_raw_content": True,
                },
            )
    except httpx.TimeoutException as error:
        raise RetryableError("tavily timed out") from error
    except httpx.TransportError as error:
        raise RetryableError(f"tavily network error: {error}") from error

    status = response.status_code
    if status == 429 or status >= 500:
        raise RetryableError(f"tavily returned {status}")
    if status != 200:
        raise FatalError(f"tavily returned {status}: {response.text[:200]}")

    results = [
        SearchResult(
            title=item.get("title") or "",
            url=item["url"],
            snippet=item.get("content") or "",
            text=item.get("raw_content"),
        )
        for item in response.json()["results"]
    ]
    ms = int((time.perf_counter() - start) * 1000)
    log.info("search provider=tavily results=%d ms=%d query=%r", len(results), ms, query)
    return results