from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .base import PaginatedResponse


class SentimentQuery(BaseModel):
    """Query parameters for sentiment analysis."""

    from_date: Optional[datetime] = Field(
        None, description="Start date for sentiment analysis"
    )
    to_date: Optional[datetime] = Field(
        None, description="End date for sentiment analysis"
    )
    meeting_uuid: Optional[str] = Field(None, description="UUID of the meeting")


class MeetingSentiment(BaseModel):
    """Represents sentiment analysis for a meeting."""

    uuid: str = Field(..., description="UUID of the sentiment analysis")
    meeting_uuid: str = Field(..., description="UUID of the meeting")
    sentiment_score: float = Field(..., description="Overall sentiment score")
    created_at: datetime = Field(..., description="When the sentiment was created")
    updated_at: datetime = Field(..., description="When the sentiment was last updated")


class MeetingSentimentsList(PaginatedResponse):
    """List of meeting sentiments with pagination."""

    results: List[MeetingSentiment] = Field(default_factory=list)
