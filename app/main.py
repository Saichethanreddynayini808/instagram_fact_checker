"""
STEP 7. FastAPI app. Thin: validate request, call pipeline.check, return Report.

POST /check  {text | url}  -> Report
GET  /check/{id}           -> Report
GET  /health
Also: request size limit and a simple per-IP rate limit.
Imports: pipeline, storage, schemas, config, log.
"""
