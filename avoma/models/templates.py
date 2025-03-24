from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class MeetingType(BaseModel):
    """Model for meeting type information."""

    uuid: UUID
    """Unique identifier for the meeting type"""

    label: str
    """Display label for the meeting type"""


class Template(BaseModel):
    """Model for a note template."""

    uuid: UUID
    """Unique identifier for the template"""

    name: str
    """Display name of the template"""

    meeting_types: List[MeetingType]
    """List of meeting types this template applies to"""

    is_default: bool
    """Whether this is a default template"""

    privacy: str
    """Privacy level (private or organization)"""

    text_slate: str
    """JSON string containing the template structure"""

    email: Optional[str] = None
    """Email of the template owner"""


class TemplateCreate(BaseModel):
    """Model for creating a new template."""

    name: str
    """Display name for the new template"""

    categories: List[UUID]
    """List of custom category UUIDs to include"""

    meeting_type_uuids: List[UUID]
    """List of meeting type UUIDs this template applies to"""

    email: Optional[str] = None
    """Email of the template owner (defaults to oldest admin if not provided)"""


class TemplateUpdate(TemplateCreate):
    """Model for updating an existing template."""

    pass
