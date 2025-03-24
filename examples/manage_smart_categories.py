import asyncio
import os
from uuid import UUID

from avoma import AvomaClient
from avoma.models.smart_categories import SmartCategoryCreate, SmartCategoryUpdate


async def main():
    # Get API key from environment variable
    api_key = os.getenv("AVOMA_API_KEY")
    if not api_key:
        raise ValueError("AVOMA_API_KEY environment variable is required")

    # Create client
    async with AvomaClient(api_key) as client:
        # List all smart categories
        categories = await client.smart_categories.list()
        print(f"\nFound {len(categories)} smart categories:")
        for category in categories:
            print(f"\nCategory: {category.name}")
            print(f"Keywords: {len(category.keywords)}")
            print(f"Prompts: {len(category.prompts)}")
            print("Settings:")
            print(f"- Bookmark and highlight: {category.settings.aug_notes_enabled}")
            print(f"- Keyword notes: {category.settings.keyword_notes_enabled}")
            print(f"- Prompt extract length: {category.settings.prompt_extract_length}")

        # Create a new category
        new_category = SmartCategoryCreate(
            name="Customer Pain Points",
            keywords=[
                "challenge",
                "problem",
                "issue",
                "difficult",
                "struggle",
                "frustrating",
            ],
            prompts=[
                "What challenges are you facing?",
                "What problems are you trying to solve?",
                "What's the biggest pain point?",
            ],
            settings={
                "aug_notes_enabled": True,
                "keyword_notes_enabled": True,
                "keyword_tracking_enabled": True,
                "prompt_extract_length": "medium",
                "prompt_extract_strategy": "after",
                "prompt_notes_enabled": True,
            },
        )

        created = await client.smart_categories.create(new_category)
        print(f"\nCreated new category: {created.name}")
        print(f"UUID: {created.uuid}")

        # Update the category settings
        update = SmartCategoryUpdate(
            keywords=new_category.keywords + ["bottleneck", "roadblock"],
            prompts=new_category.prompts,
            settings={
                **new_category.settings.model_dump(),
                "prompt_extract_length": "long",
            },
        )

        updated = await client.smart_categories.update(created.uuid, update)
        print(f"\nUpdated category {updated.name}")
        print(f"New extract length: {updated.settings.prompt_extract_length}")


if __name__ == "__main__":
    asyncio.run(main())
