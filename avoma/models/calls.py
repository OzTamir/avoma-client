from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from .base import PaginatedResponse


class CallParticipant(BaseModel):
    """Model for call participant information."""

    uuid: UUID
    """Unique identifier for the participant"""

    email: str
    """Participant's email address"""

    name: str
    """Participant's full name"""

    role: str
    """Participant's role in the call (host, attendee, etc.)"""

    joined_at: Optional[datetime] = None
    """When the participant joined the call"""

    left_at: Optional[datetime] = None
    """When the participant left the call"""


class CallStatus(BaseModel):
    """Model for call status information."""

    state: str
    """Current state of the call (scheduled, in_progress, completed, cancelled)"""

    started_at: Optional[datetime] = None
    """When the call started"""

    ended_at: Optional[datetime] = None
    """When the call ended"""

    duration: Optional[int] = None
    """Duration of the call in seconds"""


class Call(BaseModel):
    """Model for call information."""

    uuid: UUID
    """Unique identifier for the call"""

    title: str
    """Title or subject of the call"""

    description: Optional[str] = None
    """Description or agenda of the call"""

    created: datetime
    """When the call was created"""

    modified: datetime
    """When the call was last modified"""

    scheduled_start: datetime
    """Scheduled start time of the call"""

    scheduled_duration: int
    """Scheduled duration in minutes"""

    status: CallStatus
    """Current status of the call"""

    participants: List[CallParticipant]
    """List of call participants"""

    host: CallParticipant
    """Host of the call"""

    meeting_url: Optional[str] = None
    """URL for joining the call"""

    recording_available: bool
    """Whether a recording is available for this call"""

    transcription_available: bool
    """Whether a transcription is available for this call"""

    calendar_event_id: Optional[str] = None
    """External calendar event ID if synced"""

    integration_type: Optional[str] = None
    """Type of calendar/meeting integration (zoom, teams, etc.)"""


class CallsList(PaginatedResponse[Call]):
    """Model for paginated calls list response."""

    pass


class CallCreate(BaseModel):
    """Model for creating a new call."""

    title: str
    """Title or subject of the call"""

    description: Optional[str] = None
    """Description or agenda of the call"""

    scheduled_start: datetime
    """Scheduled start time of the call"""

    scheduled_duration: int
    """Scheduled duration in minutes"""

    host_email: str
    """Email of the call host"""

    participant_emails: List[str]
    """List of participant email addresses"""

    integration_type: Optional[str] = None
    """Type of calendar/meeting integration to use"""


class CallUpdate(BaseModel):
    """Model for updating an existing call."""

    title: Optional[str] = None
    """Title or subject of the call"""

    description: Optional[str] = None
    """Description or agenda of the call"""

    scheduled_start: Optional[datetime] = None
    """Scheduled start time of the call"""

    scheduled_duration: Optional[int] = None
    """Scheduled duration in minutes"""

    participant_emails: Optional[List[str]] = None
    """List of participant email addresses"""


class CallsQuery(BaseModel):
    """Model for calls query parameters."""

    from_date: str
    """Start date-time in ISO format to filter calls by"""

    to_date: str
    """End date-time in ISO format to filter calls by"""

    host_email: Optional[str] = None
    """Filter calls by host email"""

    participant_email: Optional[str] = None
    """Filter calls by participant email"""

    status: Optional[str] = None
    """Filter calls by status"""
