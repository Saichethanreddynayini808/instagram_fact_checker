"""
STEP 3. SQLite cache for search results, LLM calls, transcripts, pages.

key = sha256(kind + model + prompt file hash + request)
live: bypass | record: call and save | replay: saved only, a miss raises.
"""
