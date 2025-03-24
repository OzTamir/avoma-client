import asyncio
import os
from datetime import datetime, timedelta
from uuid import UUID

from avoma import AvomaClient


async def main():
    # Get API key from environment variable
    api_key = os.getenv("AVOMA_API_KEY")
    if not api_key:
        raise ValueError("AVOMA_API_KEY environment variable is required")

    # Create client
    async with AvomaClient(api_key) as client:
        # Set date range for last 7 days
        to_date = datetime.utcnow()
        from_date = to_date - timedelta(days=7)

        # List all notes in JSON format
        notes = await client.notes.list(
            from_date=from_date.isoformat(), to_date=to_date.isoformat()
        )
        print(f"\nFound {notes.count} notes in the last 7 days:")
        for note in notes.results:
            print(f"\nNote created: {note.created}")
            print(f"Last modified: {note.modified}")
            if isinstance(note.data, dict):
                for section in note.data.get("sections", []):
                    print(f"\nSection: {section.get('title')}")
                    for item in section.get("items", []):
                        print(f"- {item}")

        # List notes for a specific meeting in markdown format
        meeting_uuid = UUID(
            "123e4567-e89b-12d3-a456-426614174000"
        )  # Replace with actual UUID
        meeting_notes = await client.notes.list(
            from_date=from_date.isoformat(),
            to_date=to_date.isoformat(),
            meeting_uuid=meeting_uuid,
            output_format="markdown",
        )
        if meeting_notes.results:
            print(f"\nNotes for meeting {meeting_uuid}:")
            print(meeting_notes.results[0].data)

        # List notes for a specific custom category
        category_uuid = UUID(
            "123e4567-e89b-12d3-a456-426614174001"
        )  # Replace with actual UUID
        category_notes = await client.notes.list(
            from_date=from_date.isoformat(),
            to_date=to_date.isoformat(),
            custom_category=category_uuid,
        )
        print(f"\nFound {category_notes.count} notes in category {category_uuid}")


if __name__ == "__main__":
    asyncio.run(main())
