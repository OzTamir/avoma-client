from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from .base import PaginatedResponse


class UserRole(BaseModel):
    """Model for user role information."""

    uuid: UUID
    """Unique identifier for the role"""

    name: str
    """Name of the role"""

    permissions: List[str]
    """List of permissions granted to this role"""


class User(BaseModel):
    """Model for user information."""

    uuid: UUID
    """Unique identifier for the user"""

    email: str
    """User's email address"""

    first_name: str
    """User's first name"""

    last_name: str
    """User's last name"""

    created: datetime
    """When the user was created"""

    modified: datetime
    """When the user was last modified"""

    role: UserRole
    """User's role and permissions"""

    is_active: bool
    """Whether the user account is active"""

    last_login: Optional[datetime] = None
    """When the user last logged in"""

    timezone: Optional[str] = None
    """User's timezone"""

    department: Optional[str] = None
    """User's department"""

    title: Optional[str] = None
    """User's job title"""


class UsersList(PaginatedResponse[User]):
    """Model for paginated users list response."""

    pass


class UserCreate(BaseModel):
    """Model for creating a new user."""

    email: str
    """User's email address"""

    first_name: str
    """User's first name"""

    last_name: str
    """User's last name"""

    role_uuid: UUID
    """UUID of the role to assign to the user"""

    timezone: Optional[str] = None
    """User's timezone"""

    department: Optional[str] = None
    """User's department"""

    title: Optional[str] = None
    """User's job title"""


class UserUpdate(BaseModel):
    """Model for updating an existing user."""

    first_name: Optional[str] = None
    """User's first name"""

    last_name: Optional[str] = None
    """User's last name"""

    role_uuid: Optional[UUID] = None
    """UUID of the role to assign to the user"""

    is_active: Optional[bool] = None
    """Whether the user account is active"""

    timezone: Optional[str] = None
    """User's timezone"""

    department: Optional[str] = None
    """User's department"""

    title: Optional[str] = None
    """User's job title"""
