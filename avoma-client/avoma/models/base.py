from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import UUID
from pydantic import BaseModel, EmailStr

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Base model for paginated responses."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[T]


class User(BaseModel):
    """Base model for user information."""

    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    job_function: Optional[str] = None
    position: Optional[str] = None
    profile_pic: Optional[str] = None


class Role(BaseModel):
    """Base model for role information."""

    description: Optional[str] = None
    display_name: str
    name: Optional[str] = None
    role_type: str
    uuid: Optional[UUID] = None


class UserWithRole(BaseModel):
    """Base model for user with role information."""

    user: User
    role: Role
    uuid: UUID
    active: Optional[str] = None
    is_admin: Optional[bool] = None
    position: Optional[str] = None
    status: Optional[str] = None
    teams: Optional[str] = None


class MeetingAttribute(BaseModel):
    """Base model for meeting attributes like purpose and outcome."""

    label: str
    uuid: UUID
