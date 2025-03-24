import asyncio
import logging
import os
from uuid import UUID

from avoma import AvomaClient


async def main():
    # API key should be stored securely, e.g., as an environment variable
    api_key = os.environ.get("AVOMA_API_KEY", "your-api-key")

    # Create client with custom log level
    async with AvomaClient(
        api_key=api_key,
        log_level=logging.DEBUG,
        logger_name="avoma-example",  # Custom logger name
    ) as client:
        # List meetings
        meetings = await client.meetings.list(
            from_date="2023-01-01T00:00:00Z",
            to_date="2023-01-31T23:59:59Z",
            page_size=10,
        )

        # If meetings exist, get details for the first one
        if meetings.results:
            meeting = meetings.results[0]
            meeting_uuid = UUID(meeting.uuid)

            # Get meeting details
            meeting_details = await client.meetings.get(meeting_uuid)

            # Get meeting insights
            insights = await client.meetings.get_insights(meeting_uuid)

            # Print some information
            print(f"Meeting Title: {meeting_details.title}")
            print(f"AI Notes: {insights.ai_notes}")


# Advanced example with custom formatter
async def advanced_example():
    import sys

    # Create custom handler
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    # Create client with custom handler
    client = AvomaClient(api_key="your-api-key", log_level=logging.DEBUG)

    # Replace default handler with custom one
    for h in client.logger.handlers:
        client.logger.removeHandler(h)
    client.logger.addHandler(handler)

    # Now use the client as normal
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
