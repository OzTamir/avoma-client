import asyncio
import os
from datetime import datetime, timedelta
from uuid import UUID

from avoma import AvomaClient


async def main():
    # Get API key from environment variable
    api_key = os.getenv("AVOMA_API_KEY")
    if not api_key:
        raise ValueError("AVOMA_API_KEY environment variable is not set")

    async with AvomaClient(api_key) as client:
        # List sentiment analyses from the past week
        to_date = datetime.utcnow()
        from_date = to_date - timedelta(days=7)
        sentiments = await client.sentiments.list(
            from_date=from_date.isoformat() + "Z",
            to_date=to_date.isoformat() + "Z",
            status="completed",  # Only get completed analyses
        )
        print(f"Found {sentiments.count} sentiment analyses in the past week")

        # Print details of each sentiment analysis
        for sentiment in sentiments.results:
            print(f"\nMeeting: {sentiment.meeting_uuid}")
            print("Overall sentiment scores:")
            print(f"  Positive: {sentiment.overall_scores.positive:.2%}")
            print(f"  Neutral: {sentiment.overall_scores.neutral:.2%}")
            print(f"  Negative: {sentiment.overall_scores.negative:.2%}")

            # Print segments with strong positive or negative sentiment
            threshold = 0.7  # 70% confidence threshold
            print("\nHighlight segments:")
            for segment in sentiment.segments:
                if segment.scores.positive >= threshold:
                    print(f"\nPositive segment from {segment.speaker}:")
                    print(f"  '{segment.text}'")
                    print(f"  Time: {segment.start_time} - {segment.end_time}")
                    print(f"  Score: {segment.scores.positive:.2%} positive")
                elif segment.scores.negative >= threshold:
                    print(f"\nNegative segment from {segment.speaker}:")
                    print(f"  '{segment.text}'")
                    print(f"  Time: {segment.start_time} - {segment.end_time}")
                    print(f"  Score: {segment.scores.negative:.2%} negative")

        # Request sentiment analysis for a specific meeting
        meeting_uuid = UUID("123e4567-e89b-12d3-a456-426614174000")  # Example UUID
        try:
            # Request analysis
            sentiment = await client.sentiments.analyze(meeting_uuid)
            print(f"\nRequested sentiment analysis for meeting {meeting_uuid}")
            print(f"Status: {sentiment.status}")

            # If the analysis is pending, we can get its current status
            if sentiment.status == "pending":
                updated_sentiment = await client.sentiments.get(meeting_uuid)
                print(f"Current status: {updated_sentiment.status}")
                if updated_sentiment.status == "completed":
                    print("Analysis completed!")
                    print(
                        f"Overall positive sentiment: {updated_sentiment.overall_scores.positive:.2%}"
                    )
                elif updated_sentiment.status == "failed":
                    print(f"Analysis failed: {updated_sentiment.error_message}")
        except Exception as e:
            print(f"Error analyzing meeting: {e}")


if __name__ == "__main__":
    asyncio.run(main())
