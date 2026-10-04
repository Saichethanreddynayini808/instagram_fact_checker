# factchecker

Takes text, an article URL or a video URL; extracts factual claims; researches
each in parallel; returns a verdict with cited sources and a confidence score.

Core rule: every factual statement in a verdict links to a source the system
actually opened. UNVERIFIABLE is a valid answer.

## Step 0 - setup

    poetry install
    poetry add fastapi "uvicorn[standard]" pydantic pydantic-settings openai httpx trafilatura yt-dlp pyyaml streamlit langfuse
    poetry add --group dev pytest pytest-asyncio import-linter ruff
    copy .env.example .env
    git init
    poetry run python -c "from app.config import settings; print(settings.max_claims)"

The last command must print 5.

## Layers (imports point down only)

    main / ui / eval
      -> pipeline
        -> stages, ingest
          -> tools, credibility, scoring, storage
            -> schemas, config, log

## Cut from scope (reason and how to add later) - to be written in Step 8
