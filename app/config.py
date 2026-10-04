"""All settings in one place. Nothing else in the project reads os.environ.

Values come from, in order: real environment variables, then .env, then the
defaults below. API keys default to "" so tests and replay mode run without
any keys; the code that uses a key is responsible for failing clearly if it
is missing.
"""
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    # keys
    openai_api_key: str = ""
    tavily_api_key: str = ""
    serper_api_key: str = ""
    google_factcheck_api_key: str = ""
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""

    # models (names live here only; check they are current before Step 2)
    model_strong: str = "gpt-6.1-sol"
    model_fast: str = "gpt-6-luna"
    model_transcribe: str = "gpt-transcribe"

    # pipeline limits
    max_claims: int = 5
    max_research_rounds: int = 2
    check_timeout_s: int = 120

    # search fallback
    search_timeout_s: int = 10
    search_max_retries: int = 2
    breaker_fail_threshold: int = 3
    breaker_cooldown_s: int = 60

    # video
    video_full_max_s: int = 180      # up to 3 min: process fully
    video_reject_over_s: int = 900   # over 15 min: reject

    # cache and storage
    cache_mode: Literal["live", "record", "replay"] = "live"
    cache_path: Path = ROOT / "data" / "cache.db"
    storage_path: Path = ROOT / "data" / "reports.db"

    log_level: str = "INFO"


settings = Settings()
