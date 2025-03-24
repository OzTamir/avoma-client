import asyncio
import os
from datetime import datetime, timedelta

from avoma import AvomaClient


async def main():
    # Get API key from environment variable
    api_key = os.getenv("AVOMA_API_KEY")
    if not api_key:
        raise ValueError("AVOMA_API_KEY environment variable is required")

    # Create client
    async with AvomaClient(api_key) as client:
        # Get meetings from the last 7 days
        now = datetime.utcnow()
        seven_days_ago = now - timedelta(days=7)

        # Get all meetings using pagination
        meetings = await client.meetings.list(
            from_date=seven_days_ago.isoformat(),
            to_date=now.isoformat(),
            page_size=100,  # Use maximum page size for efficiency
            follow_pagination=True,  # This will automatically fetch all pages
        )

        print(f"Found {len(meetings.results)} meetings:")
        for meeting in meetings.results:
            print(f"\nMeeting: {meeting.subject}")
            print(f"Status: {meeting.state}")
            print(f"Start time: {meeting.start_at}")
            print(f"Organizer: {meeting.organizer_email}")
            print(f"Attendees: {len(meeting.attendees)}")

            # Get insights if meeting is completed
            if meeting.state == "completed":
                insights = await client.meetings.get_insights(meeting.uuid)
                print("\nAI Notes:")
                for note in insights.ai_notes:
                    print(f"- {note.text}")

                # Get sentiment analysis
                sentiment = await client.meetings.get_sentiments(meeting.uuid)
                print(
                    f"\nOverall sentiment: {getattr(sentiment, 'sentiment_score', getattr(sentiment, 'sentiment', 'N/A'))}"
                )


if __name__ == "__main__":
    asyncio.run(main())
