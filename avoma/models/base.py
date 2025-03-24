from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import UUID
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Base model for paginated API responses."""

    count: int
    """Total number of records available"""

    next: Optional[str] = None
    """URL to fetch the next page of results, if available"""

    previous: Optional[str] = None
    """URL to fetch the previous page of results, if available"""

    results: List[T]
    """The actual results for this page"""


class User(BaseModel):
    """Base model for user information."""

    email: str
    """Email address of the user"""

    first_name: str
    """User's first name"""

    last_name: str
    """User's last name"""

    is_active: bool
    """Whether the user account is active"""

    job_function: Optional[str] = None
    """User's job function or role"""

    position: Optional[str] = None
    """User's position in the organization"""

    profile_pic: Optional[str] = None
    """URL to user's profile picture"""


class Role(BaseModel):
    """Base model for role information."""

    description: Optional[str] = None
    """Description of the role"""

    display_name: str
    """Human-readable name of the role"""

    name: Optional[str] = None
    """Internal name of the role (admin, manager, member, guest)"""

    role_type: str
    """Type of role (sys or usr)"""

    uuid: Optional[UUID] = None
    """Unique identifier for the role"""


class UserWithRole(BaseModel):
    """Base model for user with role information."""

    user: User
    """User information"""

    role: Role
    """Role information"""

    uuid: UUID
    """Unique identifier for the user-role association"""

    active: Optional[str] = None
    """Activity status"""

    is_admin: Optional[bool] = None
    """Whether the user has admin privileges"""

    position: Optional[str] = None
    """User's position"""

    status: Optional[str] = None
    """User's status"""

    teams: Optional[str] = None
    """Teams the user belongs to"""


class MeetingAttribute(BaseModel):
    """Base model for meeting attributes like purpose and outcome."""

    label: str
    """Human-readable label for the attribute"""

    uuid: UUID
    """Unique identifier for the attribute"""
