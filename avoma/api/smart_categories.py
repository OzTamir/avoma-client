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
        self.client.logger.debug("SmartCategoriesAPI initialized")

    async def list(self) -> List[SmartCategory]:
        """List all smart categories.

        Returns:
            List of smart categories
        """
        self.client.logger.debug("Listing all smart categories")
        data = await self.client._request("GET", "/smart_categories")
        categories = [SmartCategory.model_validate(item) for item in data["results"]]
        self.client.logger.debug(f"Retrieved {len(categories)} smart categories")
        return categories

    async def get(self, uuid: UUID) -> SmartCategory:
        """Get a single smart category by UUID.

        Args:
            uuid: Smart category UUID

        Returns:
            Smart category details
        """
        self.client.logger.debug(f"Getting smart category with UUID: {uuid}")
        data = await self.client._request("GET", f"/smart_categories/{uuid}")
        category = SmartCategory.model_validate(data)
        self.client.logger.debug(f"Retrieved smart category: {category.name}")
        return category

    async def create(self, category: SmartCategoryCreate) -> SmartCategory:
        """Create a new smart category.

        Args:
            category: Smart category creation data

        Returns:
            Created smart category
        """
        self.client.logger.debug(f"Creating smart category: {category.name}")
        data = await self.client._request(
            "POST", "/smart_categories", json=category.model_dump(exclude_unset=True)
        )
        created_category = SmartCategory.model_validate(data)
        self.client.logger.debug(f"Created smart category: {created_category.name}")
        return created_category

    async def update(self, uuid: UUID, category: SmartCategoryUpdate) -> SmartCategory:
        """Update an existing smart category.

        Args:
            uuid: Smart category UUID
            category: Smart category update data

        Returns:
            Updated smart category
        """
        self.client.logger.debug(f"Updating smart category with UUID: {uuid}")
        data = await self.client._request(
            "PATCH",
            f"/smart_categories/{uuid}",
            json=category.model_dump(exclude_unset=True),
        )
        updated_category = SmartCategory.model_validate(data)
        self.client.logger.debug(f"Updated smart category: {updated_category.name}")
        return updated_category
