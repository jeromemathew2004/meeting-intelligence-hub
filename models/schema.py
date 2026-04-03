from pydantic import BaseModel
from typing import List


class InsightItem(BaseModel):
    speaker: str
    text: str
    confidence: float
    reason: List[str]

from typing import List, Optional
class Metadata(BaseModel):
    word_count: int
    line_count: int
    char_count: int
    clean_text: Optional[str] = None
    speakers: Optional[List[str]] = []

class Insights(BaseModel):
    decisions: List[InsightItem]
    actions: List[InsightItem]


class ProcessedResponse(BaseModel):
    metadata: Metadata
    insights: Insights