"""
STEP 5. search(query) -> results or SearchFailed(reason).

per provider: timeout 10 s -> retry with growing waits (retryable only)
-> breaker. Tavily first, then Serper, then fail with the reason.
"""
