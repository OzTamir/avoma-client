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

        # List all meeting sentiments
        sentiments = await client.sentiments.list(
            from_date=from_date.isoformat(), to_date=to_date.isoformat()
        )
        print(f"\nFound {sentiments.count} sentiment analyses in the last 7 days:")
        for sentiment in sentiments.results:
            print(f"\nMeeting {sentiment.uuid}")
            print(f"Overall sentiment: {sentiment.overall_sentiment.label}")
            print(f"Score: {sentiment.overall_sentiment.score:.2f}")
            print(f"Confidence: {sentiment.overall_sentiment.confidence:.2f}")

            # Print segments with strong sentiments (confidence > 0.9)
            strong_segments = [
                seg for seg in sentiment.segments if seg.sentiment.confidence > 0.9
            ]
            if strong_segments:
                print("\nHighly confident sentiment segments:")
                for segment in strong_segments:
                    print(f"\nSpeaker: {segment.speaker}")
                    print(f"Time: {segment.start_time:.1f}s - {segment.end_time:.1f}s")
                    print(f"Text: {segment.text}")
                    print(f"Sentiment: {segment.sentiment.label}")
                    print(f"Score: {segment.sentiment.score:.2f}")

        # Get detailed sentiment analysis for a specific meeting
        meeting_uuid = UUID(
            "123e4567-e89b-12d3-a456-426614174000"
        )  # Replace with actual UUID
        try:
            meeting_sentiment = await client.sentiments.get(meeting_uuid)
            print(f"\nDetailed sentiment analysis for meeting {meeting_uuid}:")
            print(f"Created: {meeting_sentiment.created}")
            print(f"Overall sentiment: {meeting_sentiment.overall_sentiment.label}")

            # Group segments by speaker
            segments_by_speaker = {}
            for segment in meeting_sentiment.segments:
                if segment.speaker not in segments_by_speaker:
                    segments_by_speaker[segment.speaker] = []
                segments_by_speaker[segment.speaker].append(segment)

            # Print sentiment analysis by speaker
            for speaker, segments in segments_by_speaker.items():
                speaker_scores = [seg.sentiment.score for seg in segments]
                avg_score = sum(speaker_scores) / len(speaker_scores)
                print(f"\nSpeaker: {speaker}")
                print(f"Average sentiment score: {avg_score:.2f}")
                print(f"Number of segments: {len(segments)}")

        except Exception as e:
            print(f"Error getting sentiment analysis: {e}")


if __name__ == "__main__":
    asyncio.run(main())
