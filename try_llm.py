import asyncio

from app.log import setup_logging
from app.tools.search.tavily import search

setup_logging()

results = asyncio.run(search("How many states does India have?", max_results=3))
for r in results:
    size = len(r.text) if r.text else 0
    print(r.url, "|", r.title, "|", size, "characters of page text")