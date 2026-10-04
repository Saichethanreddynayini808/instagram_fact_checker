"""
STEP 2. The only file that knows the order of the stages.

check(input) -> Report:
  ingest -> intent -> claims (max 5) -> research each claim in parallel
  (asyncio.gather) -> verdict -> citation_check -> scoring -> Report
Sets log.check_id, enforces the overall timeout, records per-stage timings.
Imports: stages, ingest, scoring, schemas, config, log.
"""
