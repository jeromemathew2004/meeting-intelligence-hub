from pydantic import BaseModel
from typing import List
from typing import List, Optional

class InsightItem(BaseModel):
    speaker: str
    text: str
    confidence: float
    reason: List[str]
    due_date: Optional[str] = None

class Metadata(BaseModel):
    word_count: int
    line_count: int
    char_count: int
    clean_text: Optional[str] = None
    speakers: Optional[List[str]] = []
    meeting_date: Optional[str] = None
class Insights(BaseModel):
    decisions: List[InsightItem]
    actions: List[InsightItem]


class ProcessedResponse(BaseModel):
    metadata: Metadata
    insights: Insights