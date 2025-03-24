from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from .base import PaginatedResponse


class SentimentScore(BaseModel):
    """Model for sentiment score details."""

    score: float
    """Sentiment score value"""

    label: str
    """Sentiment label (e.g., 'positive', 'negative', 'neutral')"""

    confidence: float
    """Confidence score for the sentiment analysis"""


class SentimentSegment(BaseModel):
    """Model for a segment of text with sentiment analysis."""

    text: str
    """The text segment that was analyzed"""

    start_time: float
    """Start time of the segment in seconds"""

    end_time: float
    """End time of the segment in seconds"""

    speaker: str
    """Speaker identifier"""

    sentiment: SentimentScore
    """Sentiment analysis results for this segment"""


class MeetingSentiment(BaseModel):
    """Model for meeting sentiment analysis."""

    uuid: UUID
    """Unique identifier for the meeting"""

    created: datetime
    """When the sentiment analysis was created"""

    modified: datetime
    """When the sentiment analysis was last modified"""

    overall_sentiment: SentimentScore
    """Overall sentiment score for the entire meeting"""

    segments: List[SentimentSegment]
    """List of analyzed segments with their sentiment scores"""


class MeetingSentimentsList(PaginatedResponse[MeetingSentiment]):
    """Model for paginated meeting sentiments list response."""

    pass


class SentimentsQuery(BaseModel):
    """Model for sentiments query parameters."""

    from_date: str
    """Start date-time in ISO format to filter sentiments by"""

    to_date: str
    """End date-time in ISO format to filter sentiments by"""

    meeting_uuid: Optional[UUID] = None
    """Optional meeting UUID to filter sentiments by"""
