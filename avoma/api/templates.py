from typing import List
from uuid import UUID

from ..models.templates import Template, TemplateCreate, TemplateUpdate


class TemplatesAPI:
    """API endpoints for templates."""

    def __init__(self, client):
        self.client = client

    async def list(self) -> List[Template]:
        """List all templates.

        Returns:
            List of templates
        """
        data = await self.client._request("GET", "/template")
        return [Template.model_validate(item) for item in data]

    async def get(self, uuid: UUID) -> Template:
        """Get a single template by UUID.

        Args:
            uuid: Template UUID

        Returns:
            Template details
        """
        data = await self.client._request("GET", f"/template/{uuid}")
        return Template.model_validate(data)

    async def create(self, template: TemplateCreate) -> Template:
        """Create a new template.

        Args:
            template: Template creation data

        Returns:
            Created template
        """
        data = await self.client._request(
            "POST", "/template", json=template.model_dump(exclude_unset=True)
        )
        return Template.model_validate(data)

    async def update(self, template: TemplateUpdate) -> Template:
        """Update an existing template.

        Args:
            template: Template update data

        Returns:
            Updated template
        """
        data = await self.client._request(
            "PUT", "/template", json=template.model_dump(exclude_unset=True)
        )
        return Template.model_validate(data)
