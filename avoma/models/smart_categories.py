from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel


class SmartCategorySettings(BaseModel):
    """Settings configuration for a smart category."""

    aug_notes_enabled: bool
    """Whether bookmark and transcript highlight is enabled"""

    keyword_notes_enabled: bool
    """Whether keyword notes are enabled"""

    keyword_tracking_enabled: bool
    """Whether keyword tracking is enabled"""

    prompt_extract_length: Optional[str] = None
    """Length of prompt extracts (short, medium, long)"""

    prompt_extract_strategy: Optional[str] = None
    """Strategy for extracting prompts (after, before, contains)"""

    prompt_notes_enabled: bool
    """Whether prompt notes are enabled"""


class Keyword(BaseModel):
    """Model for a keyword in a smart category."""

    created: datetime
    """When the keyword was created"""

    custom_category: UUID
    """UUID of the category this keyword belongs to"""

    is_primary: bool
    """Whether this is a primary keyword"""

    label: str
    """Display label for the keyword"""

    uuid: UUID
    """Unique identifier for the keyword"""

    variations: List[str]
    """Alternative forms of the keyword"""


class Prompt(BaseModel):
    """Model for a prompt in a smart category."""

    created: datetime
    """When the prompt was created"""

    custom_category: UUID
    """UUID of the category this prompt belongs to"""

    label: str
    """Display label for the prompt"""

    uuid: UUID
    """Unique identifier for the prompt"""

    variations: List[str]
    """Alternative forms of the prompt"""


class SmartCategory(BaseModel):
    """Model for a smart category."""

    uuid: UUID
    """Unique identifier for the category"""

    name: str
    """Display name of the category"""

    key: str
    """Internal key for the category"""

    is_default: bool
    """Whether this is a default category"""

    keywords: List[Keyword]
    """List of keywords associated with this category"""

    prompts: List[Prompt]
    """List of prompts associated with this category"""

    settings: SmartCategorySettings
    """Configuration settings for this category"""


class SmartCategoryUpdate(BaseModel):
    """Model for updating a smart category."""

    keywords: List[str]
    """List of keyword strings to update"""

    prompts: List[str]
    """List of prompt strings to update"""

    settings: SmartCategorySettings
    """New settings configuration"""


class SmartCategoryCreate(SmartCategoryUpdate):
    """Model for creating a new smart category."""

    name: str
    """Display name for the new category"""
