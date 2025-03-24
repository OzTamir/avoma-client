from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, HttpUrl


class Recording(BaseModel):
    """Model for recording information."""

    uuid: UUID
    meeting_uuid: UUID
    audio_url: Optional[HttpUrl] = None
    video_url: Optional[HttpUrl] = None
    valid_till: Optional[datetime] = None
    message: Optional[str] = None
