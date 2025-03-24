from typing import Optional
from uuid import UUID

from ..models.users import User, UserCreate, UserUpdate, UsersList


class UsersAPI:
    """API endpoints for users."""

    def __init__(self, client):
        self.client = client
        self.client.logger.debug("UsersAPI initialized")

    async def list(self, page_size: Optional[int] = None) -> UsersList:
        """List all users.

        Args:
            page_size: Number of users per page (max 20)

        Returns:
            Paginated list of users
        """
        self.client.logger.debug("Listing all users")
        params = {}
        if page_size is not None:
            params["page_size"] = page_size

        data = await self.client._request("GET", "/users", params=params)
        users_list = UsersList.model_validate(data)
        self.client.logger.debug(f"Retrieved {len(users_list.results)} users")
        return users_list

    async def get(self, user_uuid: UUID) -> User:
        """Get a specific user by UUID.

        Args:
            user_uuid: User UUID

        Returns:
            User details
        """
        self.client.logger.debug(f"Getting user with UUID: {user_uuid}")
        data = await self.client._request("GET", f"/users/{user_uuid}")
        user = User.model_validate(data)
        self.client.logger.debug(f"Retrieved user: {user.email}")
        return user

    async def create(self, user: UserCreate) -> User:
        """Create a new user.

        Args:
            user: User creation data

        Returns:
            Created user
        """
        self.client.logger.debug(f"Creating new user with email: {user.email}")
        data = await self.client._request(
            "POST", "/users", json=user.model_dump(exclude_unset=True)
        )
        created_user = User.model_validate(data)
        self.client.logger.debug(f"Created user with UUID: {created_user.uuid}")
        return created_user

    async def update(self, user_uuid: UUID, user: UserUpdate) -> User:
        """Update an existing user.

        Args:
            user_uuid: UUID of the user to update
            user: User update data

        Returns:
            Updated user
        """
        self.client.logger.debug(f"Updating user with UUID: {user_uuid}")
        data = await self.client._request(
            "PUT", f"/users/{user_uuid}", json=user.model_dump(exclude_unset=True)
        )
        updated_user = User.model_validate(data)
        self.client.logger.debug(f"Updated user: {updated_user.email}")
        return updated_user

    async def delete(self, user_uuid: UUID) -> None:
        """Delete a user.

        Args:
            user_uuid: UUID of the user to delete
        """
        self.client.logger.debug(f"Deleting user with UUID: {user_uuid}")
        await self.client._request("DELETE", f"/users/{user_uuid}")
        self.client.logger.debug(f"User {user_uuid} deleted")

    async def get_current(self) -> User:
        """Get the currently authenticated user.

        Returns:
            Current user details
        """
        self.client.logger.debug("Getting current authenticated user")
        data = await self.client._request("GET", "/users/me")
        user = User.model_validate(data)
        self.client.logger.debug(f"Retrieved current user: {user.email}")
        return user
