from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel

from .base import PaginatedResponse


class Note(BaseModel):
    """Model for meeting notes."""

    created: datetime
    """When the note was created"""

    modified: datetime
    """When the note was last modified"""

    data: Union[Dict[str, Any], str]
    """Note content, either as JSON object or formatted string based on output_format"""


class NotesList(PaginatedResponse[Note]):
    """Model for paginated notes list response."""

    pass


class NotesQuery(BaseModel):
    """Model for notes query parameters."""

    from_date: str
    """Start date-time in ISO format to filter notes by"""

    to_date: str
    """End date-time in ISO format to filter notes by"""

    meeting_uuid: Optional[UUID] = None
    """Optional meeting UUID to filter notes by"""

    custom_category: Optional[UUID] = None
    """Optional custom category UUID to filter notes by"""

    output_format: str = "json"
    """Format of the notes data (json, html, markdown)"""
