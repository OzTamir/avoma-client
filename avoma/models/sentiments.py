from datetime import datetime
from typing import List, Optional, Dict, Any

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


class SentimentScores(BaseModel):
    """Represents sentiment scores."""

    positive: float = Field(..., description="Positive sentiment score")
    neutral: float = Field(..., description="Neutral sentiment score")
    negative: float = Field(..., description="Negative sentiment score")


class SentimentSegment(BaseModel):
    """Represents a segment of text with sentiment analysis."""

    text: str = Field(..., description="Text content of the segment")
    start_time: datetime = Field(..., description="Start time of the segment")
    end_time: datetime = Field(..., description="End time of the segment")
    speaker: str = Field(..., description="Speaker name")
    speaker_email: str = Field(..., description="Speaker email")
    scores: SentimentScores = Field(
        ..., description="Sentiment scores for this segment"
    )


class MeetingSentiment(BaseModel):
    """Represents sentiment analysis for a meeting."""

    uuid: str = Field(..., description="UUID of the sentiment analysis")
    meeting_uuid: str = Field(..., description="UUID of the meeting")
    sentiment_score: float = Field(..., description="Overall sentiment score")
    created_at: datetime = Field(..., description="When the sentiment was created")
    updated_at: datetime = Field(..., description="When the sentiment was last updated")
    overall_scores: SentimentScores = Field(..., description="Overall sentiment scores")
    segments: List[SentimentSegment] = Field(
        default_factory=list, description="Segments with sentiment analysis"
    )


class MeetingSentimentsList(PaginatedResponse):
    """List of meeting sentiments with pagination."""

    results: List[MeetingSentiment] = Field(default_factory=list)
