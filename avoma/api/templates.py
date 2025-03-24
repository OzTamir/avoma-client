from typing import List
from uuid import UUID

from ..models.templates import Template, TemplateCreate, TemplateUpdate


class TemplatesAPI:
    """API endpoints for templates."""

    def __init__(self, client):
        self.client = client
        self.client.logger.debug("TemplatesAPI initialized")

    async def list(self) -> List[Template]:
        """List all templates.

        Returns:
            List of templates
        """
        self.client.logger.debug("Listing all templates")
        data = await self.client._request("GET", "/template")
        templates = [Template.model_validate(item) for item in data]
        self.client.logger.debug(f"Retrieved {len(templates)} templates")
        return templates

    async def get(self, uuid: UUID) -> Template:
        """Get a single template by UUID.

        Args:
            uuid: Template UUID

        Returns:
            Template details
        """
        self.client.logger.debug(f"Getting template with UUID: {uuid}")
        data = await self.client._request("GET", f"/template/{uuid}")
        template = Template.model_validate(data)
        self.client.logger.debug(f"Retrieved template: {uuid}")
        return template

    async def create(self, template: TemplateCreate) -> Template:
        """Create a new template.

        Args:
            template: Template creation data

        Returns:
            Created template
        """
        self.client.logger.debug("Creating new template")
        data = await self.client._request(
            "POST", "/template", json=template.model_dump(exclude_unset=True)
        )
        created_template = Template.model_validate(data)
        self.client.logger.debug(f"Created template with UUID: {created_template.uuid}")
        return created_template

    async def update(self, template: TemplateUpdate) -> Template:
        """Update an existing template.

        Args:
            template: Template update data

        Returns:
            Updated template
        """
        self.client.logger.debug(f"Updating template with UUID: {template.uuid}")
        data = await self.client._request(
            "PUT", "/template", json=template.model_dump(exclude_unset=True)
        )
        updated_template = Template.model_validate(data)
        self.client.logger.debug(f"Updated template: {updated_template.uuid}")
        return updated_template
