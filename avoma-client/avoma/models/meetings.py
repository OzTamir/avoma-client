from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, HttpUrl

from .base import MeetingAttribute, PaginatedResponse


class Attendee(BaseModel):
    """Model for meeting attendee."""

    email: EmailStr
    name: Optional[str] = None
    response_status: str
    uuid: UUID


class CallDetails(BaseModel):
    """Model for call details."""

    external_id: str
    frm: str
    to: str


class Meeting(BaseModel):
    """Model for meeting information."""

    uuid: UUID
    subject: str
    created: datetime
    modified: datetime
    is_private: bool
    is_internal: bool
    organizer_email: EmailStr
    state: str
    attendees: List[Attendee]
    audio_ready: bool
    call_details: Optional[CallDetails] = None
    duration: Optional[float] = None
    end_at: Optional[datetime] = None
    is_call: bool
    notes_ready: bool
    outcome: Optional[MeetingAttribute] = None
    processing_status: Optional[str] = None
    purpose: Optional[MeetingAttribute] = None
    recording_uuid: Optional[UUID] = None
    start_at: Optional[datetime] = None
    transcript_ready: bool
    transcription_uuid: Optional[UUID] = None
    type: Optional[MeetingAttribute] = None
    url: Optional[HttpUrl] = None
    video_ready: bool


class MeetingList(PaginatedResponse[Meeting]):
    """Model for paginated meeting list response."""

    pass


class SpeakerStats(BaseModel):
    """Model for speaker statistics."""

    designation: str
    speaker_id: str
    value: float


class SentimentRange(BaseModel):
    """Model for sentiment range."""

    score: float
    time_range: List[float]


class MeetingSentiment(BaseModel):
    """Model for meeting sentiment."""

    sentiment: int
    sentiment_ranges: List[SentimentRange]


class Speaker(BaseModel):
    """Model for speaker information."""

    email: EmailStr
    id: int
    is_rep: bool
    name: Optional[str] = None


class AINote(BaseModel):
    """Model for AI-generated note."""

    note_type: str
    uuid: UUID
    start: float
    end: float
    text: str
    speaker_id: int


class KeywordOccurrence(BaseModel):
    """Model for keyword occurrence."""

    word: str
    count: int
    score: float


class CategoryKeywords(BaseModel):
    """Model for category keywords."""

    category: str
    count: int
    is_rep: bool
    keywords: List[KeywordOccurrence]
    speaker_id: Optional[int] = None


class MeetingInsights(BaseModel):
    """Model for meeting insights."""

    ai_notes: List[AINote]
    keywords: dict
    speakers: List[Speaker]
