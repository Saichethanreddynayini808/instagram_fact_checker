"""
STEP 2. SearchProvider protocol, SearchResult, and the two error types:
RetryableError (timeout, 5xx, 429) and FatalError (401, 400).
"""
"""What every search provider shares: the result shape and two error types."""
from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str             # short extract chosen by the search service
    text: str | None = None  # full page text, when the service supplies it


class RetryableError(Exception):
    """Worth trying again: timeout, network trouble, 429, 5xx."""


class FatalError(Exception):
    """Trying again will not help: bad key, bad request, plan limit reached."""