from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, HttpUrl


class Speaker(BaseModel):
    """Model for speaker information in a transcription."""

    email: str
    """Email address of the speaker"""

    id: int
    """Unique identifier for the speaker within the transcription"""

    is_rep: bool
    """Whether the speaker is a representative (true) or customer/prospect (false)"""

    name: Optional[str] = None
    """Optional full name of the speaker"""


class TranscriptSegment(BaseModel):
    """Model for a segment of transcribed speech."""

    transcript: str
    """The actual transcribed text"""

    timestamps: List[float]
    """List of timestamps (in seconds) for each word in the transcript, relative to recording start"""

    speaker_id: int
    """ID of the speaker who said this segment, references Speaker.id"""


class Transcription(BaseModel):
    """Model for a complete meeting transcription."""

    uuid: UUID
    """Unique identifier for the transcription"""

    transcript: List[TranscriptSegment]
    """List of transcribed segments in chronological order"""

    speakers: List[Speaker]
    """List of all speakers in the transcription"""

    transcription_vtt_url: HttpUrl
    """URL to download the transcription in VTT format"""
