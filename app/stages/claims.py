"""
STEP 2. Extract up to settings.max_claims checkable claims.

run(content: ContentObject) -> list[Claim]. One call, structured output.
Each claim must stand alone (no "he", "this year").
Imports: tools.llm, schemas, config.
"""
