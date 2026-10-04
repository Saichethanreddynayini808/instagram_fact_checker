"""
STEP 2. Analyst and verdict in one call, strong model.

run(pack: EvidencePack) -> ClaimVerdict (label, explanation, cited S-ids).
The model sees sources as S1, S2.. and never sees or writes URLs.
Empty or failed pack -> UNVERIFIABLE without calling the model.
Imports: tools.llm, schemas.
"""
