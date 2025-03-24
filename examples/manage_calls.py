import asyncio
import os
from datetime import datetime, timedelta
from uuid import UUID

from avoma import AvomaClient
from avoma.models.calls import CallCreate, CallUpdate


async def main():
    # Get API key from environment variable
    api_key = os.getenv("AVOMA_API_KEY")
    if not api_key:
        raise ValueError("AVOMA_API_KEY environment variable is not set")

    async with AvomaClient(api_key) as client:
        # List calls from the past week
        to_date = datetime.utcnow()
        from_date = to_date - timedelta(days=7)
        calls = await client.calls.list(
            from_date=from_date.isoformat() + "Z",
            to_date=to_date.isoformat() + "Z",
        )
        print(f"Found {calls.count} calls in the past week")

        # Create a new call for tomorrow
        scheduled_start = datetime.utcnow() + timedelta(days=1)
        new_call = await client.calls.create(
            CallCreate(
                title="Product Demo",
                description="Demo of our new features",
                scheduled_start=scheduled_start,
                scheduled_duration=60,  # 60 minutes
                host_email="sales@company.com",
                participant_emails=[
                    "client@prospect.com",
                    "support@company.com",
                ],
                integration_type="zoom",  # or "teams", "google_meet", etc.
            )
        )
        print(f"\nCreated new call: {new_call.title}")
        print(f"Meeting URL: {new_call.meeting_url}")
        print(f"Scheduled for: {new_call.scheduled_start}")

        # Update the call to add more participants
        updated_call = await client.calls.update(
            new_call.uuid,
            CallUpdate(
                participant_emails=[
                    "client@prospect.com",
                    "support@company.com",
                    "product@company.com",  # Added product manager
                ],
            ),
        )
        print(f"\nUpdated call participants:")
        for participant in updated_call.participants:
            print(f"- {participant.email} ({participant.role})")

        # Demonstrate call lifecycle (using a different call UUID)
        demo_uuid = UUID("123e4567-e89b-12d3-a456-426614174000")
        try:
            # Start the call
            started_call = await client.calls.start(demo_uuid)
            print(f"\nStarted call: {started_call.status.state}")
            print(f"Started at: {started_call.status.started_at}")

            # End the call
            ended_call = await client.calls.end(demo_uuid)
            print(f"Ended call: {ended_call.status.state}")
            print(f"Duration: {ended_call.status.duration} seconds")

            # Cancel a different call
            cancelled_call = await client.calls.cancel(demo_uuid)
            print(f"Cancelled call: {cancelled_call.status.state}")
        except Exception as e:
            print(f"Error demonstrating call lifecycle: {e}")


if __name__ == "__main__":
    asyncio.run(main())
