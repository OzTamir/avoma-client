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
        # Get meetings from the last day
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)

        # First get a meeting
        meetings = await client.meetings.list(
            from_date=yesterday.isoformat(), to_date=now.isoformat()
        )

        if not meetings.results:
            print("No meetings found in the last 24 hours")
            return

        # Get the first completed meeting
        meeting = next((m for m in meetings.results if m.state == "completed"), None)

        if not meeting:
            print("No completed meetings found")
            return

        print(f"Getting recording for meeting: {meeting.subject}")

        # Get the recording
        recording = await client.recordings.get_by_meeting(meeting.uuid)

        print("\nRecording details:")
        print(f"Audio URL: {recording.audio_url}")
        print(f"Video URL: {recording.video_url}")
        print(f"Valid until: {recording.valid_till}")


if __name__ == "__main__":
    asyncio.run(main())
