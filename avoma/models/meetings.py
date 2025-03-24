from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, HttpUrl

from .base import MeetingAttribute, PaginatedResponse


class Attendee(BaseModel):
    """Model for meeting attendee information."""

    email: str
    """Email address of the attendee"""

    name: Optional[str] = None
    """Full name of the attendee"""

    response_status: str
    """Response status (needsaction, accepted, declined, tentativelyaccepted)"""

    uuid: UUID
    """Unique identifier for the attendee"""


class CallDetails(BaseModel):
    """Model for call details associated with a meeting."""

    external_id: str
    """Unique identifier from the dialer integration"""

    frm: str
    """Phone number the call was made from"""

    to: str
    """Phone number the call was made to"""


class Meeting(BaseModel):
    """Model for meeting information."""

    uuid: UUID
    """Unique identifier for the meeting"""

    subject: str
    """Subject or title of the meeting"""

    created: datetime
    """When the meeting was created"""

    modified: datetime
    """When the meeting was last modified"""

    is_private: bool
    """Whether the meeting is visible only to attendees"""

    is_internal: bool
    """Whether the meeting has only internal attendees"""

    organizer_email: str
    """Email of the meeting organizer"""

    state: str
    """Meeting state (scheduled, in_progress, completed, cancelled)"""

    attendees: List[Attendee]
    """List of meeting attendees"""

    audio_ready: bool
    """Whether the audio recording is ready"""

    call_details: Optional[CallDetails] = None
    """Details of associated call, if any"""

    duration: Optional[float] = None
    """Actual duration of the meeting in seconds"""

    end_at: Optional[datetime] = None
    """Scheduled end time"""

    is_call: bool
    """Whether this is a voice call"""

    notes_ready: bool
    """Whether AI notes are ready"""

    outcome: Optional[MeetingAttribute] = None
    """Meeting outcome, if set"""

    processing_status: Optional[str] = None
    """Current processing status of the meeting"""

    purpose: Optional[MeetingAttribute] = None
    """Meeting purpose/type"""

    recording_uuid: Optional[UUID] = None
    """UUID of associated recording"""

    start_at: Optional[datetime] = None
    """Scheduled start time"""

    transcript_ready: bool
    """Whether transcription is ready"""

    transcription_uuid: Optional[UUID] = None
    """UUID of associated transcription"""

    type: Optional[MeetingAttribute] = None
    """Meeting type"""

    url: Optional[HttpUrl] = None
    """URL of the meeting (e.g., video conference link)"""

    video_ready: bool
    """Whether the video recording is ready"""


class MeetingList(PaginatedResponse[Meeting]):
    """Model for paginated meeting list response."""

    pass


class SpeakerStats(BaseModel):
    """Model for speaker statistics."""

    designation: str
    """Speaker's designation or role"""

    speaker_id: str
    """Unique identifier for the speaker"""

    value: float
    """Statistical value (e.g., talk time percentage)"""


class SentimentRange(BaseModel):
    """Model for sentiment analysis over a time range."""

    score: float
    """Sentiment score (-1 to 1)"""

    time_range: List[float]
    """Start and end time in seconds"""


class MeetingSentiment(BaseModel):
    """Model for meeting sentiment analysis."""

    sentiment: int
    """Overall sentiment score"""

    sentiment_ranges: List[SentimentRange]
    """Sentiment scores over time ranges"""


class Speaker(BaseModel):
    """Model for speaker information."""

    email: str
    """Email address of the speaker"""

    id: int
    """Unique identifier for the speaker"""

    is_rep: bool
    """Whether the speaker is a representative"""

    name: Optional[str] = None
    """Full name of the speaker"""


class AINote(BaseModel):
    """Model for AI-generated note."""

    note_type: str
    """Type of note (e.g., action_item, question)"""

    uuid: UUID
    """Unique identifier for the note"""

    start: float
    """Start time in seconds"""

    end: float
    """End time in seconds"""

    text: str
    """Content of the note"""

    speaker_id: int
    """ID of the speaker this note is about"""


class KeywordOccurrence(BaseModel):
    """Model for keyword occurrence information."""

    word: str
    """The keyword that was found"""

    count: int
    """Number of occurrences"""

    score: float
    """Relevance score"""


class CategoryKeywords(BaseModel):
    """Model for category keyword analysis."""

    category: str
    """Name of the category"""

    count: int
    """Total count of keywords in this category"""

    is_rep: bool
    """Whether these are from a representative"""

    keywords: List[KeywordOccurrence]
    """List of keyword occurrences"""

    speaker_id: Optional[int] = None
    """ID of the speaker, if applicable"""


class MeetingInsights(BaseModel):
    """Model for meeting insights including AI analysis."""

    ai_notes: List[AINote]
    """AI-generated notes from the meeting"""

    keywords: dict
    """Keyword analysis results"""

    speakers: List[Speaker]
    """List of speakers in the meeting"""
