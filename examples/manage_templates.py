import asyncio
import os
from uuid import UUID

from avoma import AvomaClient
from avoma.models.templates import TemplateCreate, TemplateUpdate


async def main():
    # Get API key from environment variable
    api_key = os.getenv("AVOMA_API_KEY")
    if not api_key:
        raise ValueError("AVOMA_API_KEY environment variable is required")

    # Create client
    async with AvomaClient(api_key) as client:
        # List all templates
        templates = await client.templates.list()
        print(f"\nFound {len(templates)} templates:")
        for template in templates:
            print(f"\nTemplate: {template.name}")
            print(f"Privacy: {template.privacy}")
            print("Meeting Types:")
            for mt in template.meeting_types:
                print(f"- {mt.label}")
            if template.email:
                print(f"Owner: {template.email}")

        # Create a new template for discovery calls
        discovery_template = TemplateCreate(
            name="Discovery Call Template",
            categories=[
                UUID("123e4567-e89b-12d3-a456-426614174001"),  # Pain Points
                UUID("123e4567-e89b-12d3-a456-426614174002"),  # Requirements
                UUID("123e4567-e89b-12d3-a456-426614174003"),  # Next Steps
            ],
            meeting_type_uuids=[
                UUID("123e4567-e89b-12d3-a456-426614174004"),  # Discovery Call
            ],
        )

        created = await client.templates.create(discovery_template)
        print(f"\nCreated new template: {created.name}")
        print(f"UUID: {created.uuid}")

        # Update the template with additional categories
        update = TemplateUpdate(
            name=discovery_template.name,
            categories=[
                *discovery_template.categories,
                UUID("123e4567-e89b-12d3-a456-426614174005"),  # Budget
            ],
            meeting_type_uuids=discovery_template.meeting_type_uuids,
        )

        updated = await client.templates.update(update)
        print(f"\nUpdated template: {updated.name}")
        print(f"Number of meeting types: {len(updated.meeting_types)}")


if __name__ == "__main__":
    asyncio.run(main())
