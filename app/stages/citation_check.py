"""
STEP 4. Deterministic. No LLM.

run(verdict, pack) -> verdict (possibly downgraded) + rejected citations
  every cited id exists in the pack
  every evidence quote appears in that source's fetched text
  (after normalising whitespace, quotes and case)
No surviving citation -> UNVERIFIABLE.
Imports: schemas.
"""
