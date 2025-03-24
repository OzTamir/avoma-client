from typing import Optional
from uuid import UUID

from ..models.users import User, UserCreate, UserUpdate, UsersList


class UsersAPI:
    """API endpoints for users."""

    def __init__(self, client):
        self.client = client

    async def list(self, page_size: Optional[int] = None) -> UsersList:
        """List all users.

        Args:
            page_size: Number of users per page (max 20)

        Returns:
            Paginated list of users
        """
        params = {}
        if page_size is not None:
            params["page_size"] = page_size

        data = await self.client._request("GET", "/users", params=params)
        return UsersList.model_validate(data)

    async def get(self, user_uuid: UUID) -> User:
        """Get a specific user by UUID.

        Args:
            user_uuid: User UUID

        Returns:
            User details
        """
        data = await self.client._request("GET", f"/users/{user_uuid}")
        return User.model_validate(data)

    async def create(self, user: UserCreate) -> User:
        """Create a new user.

        Args:
            user: User creation data

        Returns:
            Created user
        """
        data = await self.client._request(
            "POST", "/users", json=user.model_dump(exclude_unset=True)
        )
        return User.model_validate(data)

    async def update(self, user_uuid: UUID, user: UserUpdate) -> User:
        """Update an existing user.

        Args:
            user_uuid: UUID of the user to update
            user: User update data

        Returns:
            Updated user
        """
        data = await self.client._request(
            "PUT", f"/users/{user_uuid}", json=user.model_dump(exclude_unset=True)
        )
        return User.model_validate(data)

    async def delete(self, user_uuid: UUID) -> None:
        """Delete a user.

        Args:
            user_uuid: UUID of the user to delete
        """
        await self.client._request("DELETE", f"/users/{user_uuid}")

    async def get_current(self) -> User:
        """Get the currently authenticated user.

        Returns:
            Current user details
        """
        data = await self.client._request("GET", "/users/me")
        return User.model_validate(data)
