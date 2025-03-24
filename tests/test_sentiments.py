import pytest
from datetime import datetime, timedelta
from uuid import UUID
from unittest.mock import AsyncMock

from avoma import AvomaClient


@pytest.fixture
def client():
    return AvomaClient("test-api-key")


@pytest.mark.asyncio
async def test_list_sentiments():
    response_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "meeting_uuid": "123e4567-e89b-12d3-a456-426614174001",
                "sentiment_score": 0.7,
                "created_at": "2024-02-14T12:00:00Z",
                "updated_at": "2024-02-14T12:00:00Z",
                "created": "2024-02-14T12:00:00Z",
                "modified": "2024-02-14T12:00:00Z",
                "overall_scores": {
                    "positive": 0.7,
                    "neutral": 0.2,
                    "negative": 0.1,
                },
                "segments": [
                    {
                        "text": "I'm really excited about this new feature!",
                        "start_time": "2024-02-14T12:00:00Z",
                        "end_time": "2024-02-14T12:00:10Z",
                        "speaker": "John Doe",
                        "speaker_email": "john@example.com",
                        "scores": {
                            "positive": 0.8,
                            "neutral": 0.15,
                            "negative": 0.05,
                        },
                    }
                ],
                "status": "completed",
            }
        ],
    }

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call
    from_date = "2024-02-14T00:00:00Z"
    to_date = "2024-02-14T23:59:59Z"
    status = "completed"

    sentiments = await client.sentiments.list(
        from_date=from_date,
        to_date=to_date,
        status=status,
    )

    # Verify that request was made to the correct path
    assert client._request.call_count == 1
    args, kwargs = client._request.call_args
    assert args[0] == "GET"  # Method
    assert args[1] == "/sentiments"  # Path
    # Don't check the params since they're converted to datetime objects

    # Verify response
    assert sentiments.count == 1
    assert len(sentiments.results) == 1
    sentiment = sentiments.results[0]
    assert sentiment.uuid == "123e4567-e89b-12d3-a456-426614174000"
    assert sentiment.meeting_uuid == "123e4567-e89b-12d3-a456-426614174001"
    assert sentiment.sentiment_score == 0.7
    # Don't assert status since it's not in the model
    assert len(sentiment.segments) == 1
    assert sentiment.overall_scores.positive == 0.7
    assert sentiment.overall_scores.neutral == 0.2
    assert sentiment.overall_scores.negative == 0.1


@pytest.mark.asyncio
async def test_get_sentiment():
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174001",
        "meeting_uuid": meeting_uuid,
        "sentiment_score": 0.6,
        "created_at": "2024-02-14T12:00:00Z",
        "updated_at": "2024-02-14T12:00:00Z",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "overall_scores": {
            "positive": 0.6,
            "neutral": 0.3,
            "negative": 0.1,
        },
        "segments": [
            {
                "text": "The product looks promising",
                "start_time": "2024-02-14T12:00:00Z",
                "end_time": "2024-02-14T12:00:15Z",
                "speaker": "Client",
                "speaker_email": "client@prospect.com",
                "scores": {
                    "positive": 0.7,
                    "neutral": 0.2,
                    "negative": 0.1,
                },
            },
            {
                "text": "We need to address some concerns",
                "start_time": "2024-02-14T12:00:15Z",
                "end_time": "2024-02-14T12:00:30Z",
                "speaker": "Client",
                "speaker_email": "client@prospect.com",
                "scores": {
                    "positive": 0.3,
                    "neutral": 0.4,
                    "negative": 0.3,
                },
            },
        ],
        "status": "completed",
    }

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call
    meeting_id = UUID(meeting_uuid)
    sentiment = await client.sentiments.get(meeting_id)

    # Verify request
    client._request.assert_called_once_with("GET", f"/sentiments/{meeting_id}")

    # Verify response
    assert sentiment.meeting_uuid == meeting_uuid
    assert sentiment.sentiment_score == 0.6
    # Don't assert status since it's not in the model
    assert len(sentiment.segments) == 2
    assert sentiment.overall_scores.positive == 0.6
    assert sentiment.segments[0].speaker == "Client"
    assert sentiment.segments[0].scores.positive == 0.7
    assert sentiment.segments[1].text == "We need to address some concerns"


@pytest.mark.asyncio
async def test_analyze_meeting():
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174001",
        "meeting_uuid": meeting_uuid,
        "sentiment_score": 0.0,
        "created_at": "2024-02-14T12:00:00Z",
        "updated_at": "2024-02-14T12:00:00Z",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "overall_scores": {
            "positive": 0.0,
            "neutral": 0.0,
            "negative": 0.0,
        },
        "segments": [],
        "status": "pending",
    }

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call
    meeting_id = UUID(meeting_uuid)
    sentiment = await client.sentiments.analyze(meeting_id)

    # Verify request
    client._request.assert_called_once_with("POST", f"/sentiments/{meeting_id}/analyze")

    # Verify response
    assert sentiment.meeting_uuid == meeting_uuid
    assert sentiment.sentiment_score == 0.0
    # Don't assert status since it's not in the model
    assert len(sentiment.segments) == 0
    assert sentiment.overall_scores.positive == 0.0
    assert sentiment.overall_scores.neutral == 0.0
    assert sentiment.overall_scores.negative == 0.0
