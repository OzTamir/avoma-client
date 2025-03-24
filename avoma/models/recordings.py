from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, HttpUrl


class Recording(BaseModel):
    """Model for meeting recording information."""

    uuid: UUID
    """Unique identifier for the recording"""

    meeting_uuid: UUID
    """UUID of the meeting this recording belongs to"""

    audio_url: Optional[HttpUrl] = None
    """Pre-signed URL to download the audio recording"""

    video_url: Optional[HttpUrl] = None
    """Pre-signed URL to download the video recording"""

    valid_till: Optional[datetime] = None
    """When the pre-signed URLs will expire"""

    message: Optional[str] = None
    """Optional message about the recording status"""
