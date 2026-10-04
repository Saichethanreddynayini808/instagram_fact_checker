"""Logging setup. Call setup_logging() once at start-up (main, ui, eval).

Every log line carries a check_id, so when five claims are researched in
parallel you can still filter the lines belonging to one check.

Usage in any module:
    import logging
    log = logging.getLogger(__name__)
    log.info("search ok provider=%s results=%d ms=%d", name, n, ms)
"""
import logging
from contextvars import ContextVar

# Set once per check in pipeline.py; asyncio tasks inherit it automatically.
check_id: ContextVar[str] = ContextVar("check_id", default="-")


class _CheckIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.check_id = check_id.get()
        return True


def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler()
    handler.addFilter(_CheckIdFilter())
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)-7s [%(check_id)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level)
    # Third-party libraries are noisy at INFO.
    for noisy in ("httpx", "httpx2", "httpcore", "openai"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
