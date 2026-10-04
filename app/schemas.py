"""
STEP 1. Data shapes shared by every layer. Imports: nothing from app.

ContentObject  what came in (text, source url, kind, duration)
Claim          one checkable statement (id C1..C5, text)
Source         one page we opened (id S1.., url, domain, credibility, text)
Evidence       source_id + exact quote + stance (supports/refutes/neutral)
EvidencePack   claim + its sources + its evidence + search failure reason
ClaimVerdict   label, explanation, cited source ids, confidence
Report         content + verdicts + timings + cost

Rules enforced here, not in prompts: labels are a fixed Literal; a verdict may
only cite source ids present in its EvidencePack; confidence is 0..1.
"""


"""Data shapes shared by every layer. Imports nothing from app.

Order follows the pipeline:
ContentObject -> Claim -> Source / Evidence -> EvidencePack
-> VerdictDraft -> ClaimVerdict -> Report
"""
from typing import Annotated, Literal

from pydantic import BaseModel, Field

# ---- fixed choices and reusable rules -------------------------------------

Label = Literal["TRUE", "FALSE", "MISLEADING", "UNVERIFIABLE", "SATIRE"]
Stance = Literal["supports", "refutes", "neutral"]
ContentKind = Literal["text", "article", "video"]

# "A string that looks like S1, S2, ..." - written once, used in four places.
SourceId = Annotated[str, Field(pattern=r"^S\d+$")]


# ---- input ----------------------------------------------------------------

class ContentObject(BaseModel):
    """Whatever came in, after ingest turned it into plain text."""

    kind: ContentKind
    text: str = Field(min_length=1)
    url: str | None = None           # None when the user pasted text
    duration_s: float | None = None  # video only
    truncated: bool = False          # True when only the first 3 minutes were used


class Claim(BaseModel):
    """One statement to check."""

    id: str = Field(pattern=r"^C\d+$")
    text: str = Field(min_length=1)


# ---- research -------------------------------------------------------------

class Source(BaseModel):
    """One page the system actually opened."""

    id: SourceId
    url: str
    domain: str
    credibility: float = Field(ge=0, le=1)
    text: str


class Evidence(BaseModel):
    """One exact quote from one source."""

    source_id: SourceId
    quote: str = Field(min_length=1)
    stance: Stance


class EvidencePack(BaseModel):
    """Everything found about one claim. Empty lists are allowed:
    that is what a failed search looks like, and it leads to UNVERIFIABLE."""

    claim: Claim
    sources: list[Source] = []
    evidence: list[Evidence] = []
    failure_reason: str | None = None


# ---- verdict --------------------------------------------------------------

class VerdictDraft(BaseModel):
    """What the model returns. No confidence field: the model never sets it."""

    label: Label
    explanation: str = Field(min_length=1)
    cited_source_ids: list[SourceId] = []


class ClaimVerdict(BaseModel):
    """The final verdict for one claim, built by code from a VerdictDraft."""

    claim: Claim
    label: Label
    explanation: str = Field(min_length=1)
    cited_source_ids: list[SourceId] = []
    rejected_source_ids: list[SourceId] = []  # citations that failed the check
    sources: list[Source] = []                # the cited pages, so the UI can link them
    confidence: float = Field(ge=0, le=1)


# ---- output ---------------------------------------------------------------

class Report(BaseModel):
    """The single thing returned to the user, stored, and scored."""

    content: ContentObject
    verdicts: list[ClaimVerdict]
    duration_s: float = Field(ge=0)
    cost_usd: float = Field(ge=0)