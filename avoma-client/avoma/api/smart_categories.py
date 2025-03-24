from typing import List, Optional
from uuid import UUID

from ..models.smart_categories import (
    SmartCategory,
    SmartCategoryCreate,
    SmartCategoryUpdate,
)


class SmartCategoriesAPI:
    """API endpoints for smart categories."""

    def __init__(self, client):
        self.client = client

    async def list(self) -> List[SmartCategory]:
        """List all smart categories.

        Returns:
            List of smart categories
        """
        data = await self.client._request("GET", "/smart_categories")
        return [SmartCategory.model_validate(item) for item in data["results"]]

    async def get(self, uuid: UUID) -> SmartCategory:
        """Get a single smart category by UUID.

        Args:
            uuid: Smart category UUID

        Returns:
            Smart category details
        """
        data = await self.client._request("GET", f"/smart_categories/{uuid}")
        return SmartCategory.model_validate(data)

    async def create(self, category: SmartCategoryCreate) -> SmartCategory:
        """Create a new smart category.

        Args:
            category: Smart category creation data

        Returns:
            Created smart category
        """
        data = await self.client._request(
            "POST", "/smart_categories", json=category.model_dump(exclude_unset=True)
        )
        return SmartCategory.model_validate(data)

    async def update(self, uuid: UUID, category: SmartCategoryUpdate) -> SmartCategory:
        """Update an existing smart category.

        Args:
            uuid: Smart category UUID
            category: Smart category update data

        Returns:
            Updated smart category
        """
        data = await self.client._request(
            "PATCH",
            f"/smart_categories/{uuid}",
            json=category.model_dump(exclude_unset=True),
        )
        return SmartCategory.model_validate(data)
