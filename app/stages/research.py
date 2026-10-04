"""
STEP 2. The only stage with a loop (max settings.max_research_rounds).

run(claim: Claim) -> EvidencePack
  round: write queries -> search -> fetch pages -> extract exact quotes
  if evidence is thin, write new queries and do one more round
Never raises on search failure: returns a pack with the failure reason.
Imports: tools.llm, tools.search, tools.fetch, credibility, schemas, config.
"""
