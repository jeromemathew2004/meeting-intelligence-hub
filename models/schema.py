from pydantic import BaseModel
from typing import List


class InsightItem(BaseModel):
    speaker: str
    text: str
    confidence: float
    reason: List[str]


class Metadata(BaseModel):
    word_count: int
    line_count: int
    char_count: int


class Insights(BaseModel):
    decisions: List[InsightItem]
    actions: List[InsightItem]


class ProcessedResponse(BaseModel):
    metadata: Metadata
    insights: Insights