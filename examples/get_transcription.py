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

        print(f"Getting transcription for meeting: {meeting.subject}")

        # Get transcriptions for the meeting
        transcriptions = await client.transcriptions.list(
            from_date=yesterday.isoformat(),
            to_date=now.isoformat(),
            meeting_uuid=meeting.uuid,
        )

        if not transcriptions:
            print("No transcriptions found for this meeting")
            return

        transcription = transcriptions[0]
        print("\nTranscription details:")
        print(f"UUID: {transcription.uuid}")
        print(f"VTT URL: {transcription.transcription_vtt_url}")
        print("\nSpeakers:")
        for speaker in transcription.speakers:
            print(
                f"- {speaker.name or speaker.email} ({'Rep' if speaker.is_rep else 'Customer'})"
            )

        print("\nTranscript:")
        for segment in transcription.transcript:
            speaker = next(
                s for s in transcription.speakers if s.id == segment.speaker_id
            )
            speaker_name = speaker.name or speaker.email
            print(f"{speaker_name}: {segment.transcript}")


if __name__ == "__main__":
    asyncio.run(main())
