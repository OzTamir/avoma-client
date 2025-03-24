import pytest
from datetime import datetime, timedelta
from uuid import UUID

from aioresponses import aioresponses
from avoma import AvomaClient


@pytest.fixture
def client():
    return AvomaClient("test-api-key")


@pytest.fixture
def mock_api():
    with aioresponses() as m:
        yield m


@pytest.mark.asyncio
async def test_list_sentiments(client, mock_api):
    response_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "meeting_uuid": "123e4567-e89b-12d3-a456-426614174001",
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

    mock_api.get(
        "https://api.avoma.com/v1/sentiments",
        payload=response_data,
        params={
            "from_date": "2024-02-14T00:00:00Z",
            "to_date": "2024-02-14T23:59:59Z",
            "status": "completed",
        },
    )

    sentiments = await client.sentiments.list(
        from_date="2024-02-14T00:00:00Z",
        to_date="2024-02-14T23:59:59Z",
        status="completed",
    )

    assert sentiments.count == 1
    assert len(sentiments.results) == 1
    sentiment = sentiments.results[0]
    assert isinstance(sentiment.uuid, UUID)
    assert isinstance(sentiment.meeting_uuid, UUID)
    assert sentiment.status == "completed"
    assert len(sentiment.segments) == 1
    assert sentiment.overall_scores.positive == 0.7
    assert sentiment.overall_scores.neutral == 0.2
    assert sentiment.overall_scores.negative == 0.1


@pytest.mark.asyncio
async def test_get_sentiment(client, mock_api):
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174001",
        "meeting_uuid": meeting_uuid,
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

    mock_api.get(
        f"https://api.avoma.com/v1/sentiments/{meeting_uuid}",
        payload=response_data,
    )

    sentiment = await client.sentiments.get(UUID(meeting_uuid))

    assert str(sentiment.meeting_uuid) == meeting_uuid
    assert sentiment.status == "completed"
    assert len(sentiment.segments) == 2
    assert sentiment.overall_scores.positive == 0.6
    assert sentiment.segments[0].speaker == "Client"
    assert sentiment.segments[0].scores.positive == 0.7
    assert sentiment.segments[1].text == "We need to address some concerns"


@pytest.mark.asyncio
async def test_analyze_meeting(client, mock_api):
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174001",
        "meeting_uuid": meeting_uuid,
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

    mock_api.post(
        f"https://api.avoma.com/v1/sentiments/{meeting_uuid}/analyze",
        payload=response_data,
    )

    sentiment = await client.sentiments.analyze(UUID(meeting_uuid))

    assert str(sentiment.meeting_uuid) == meeting_uuid
    assert sentiment.status == "pending"
    assert len(sentiment.segments) == 0
    assert sentiment.overall_scores.positive == 0.0
    assert sentiment.overall_scores.neutral == 0.0
    assert sentiment.overall_scores.negative == 0.0
