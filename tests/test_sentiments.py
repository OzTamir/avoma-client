import pytest
from datetime import datetime
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
                "created": "2024-02-14T12:00:00Z",
                "modified": "2024-02-14T12:00:00Z",
                "overall_sentiment": {
                    "score": 0.8,
                    "label": "positive",
                    "confidence": 0.95,
                },
                "segments": [
                    {
                        "text": "We're excited about this partnership",
                        "start_time": 120.5,
                        "end_time": 123.8,
                        "speaker": "John",
                        "sentiment": {
                            "score": 0.9,
                            "label": "positive",
                            "confidence": 0.98,
                        },
                    }
                ],
            }
        ],
    }

    mock_api.get(
        "https://api.avoma.com/v1/sentiments",
        payload=response_data,
        params={
            "from_date": "2024-02-14T00:00:00Z",
            "to_date": "2024-02-14T23:59:59Z",
        },
    )

    sentiments = await client.sentiments.list(
        from_date="2024-02-14T00:00:00Z", to_date="2024-02-14T23:59:59Z"
    )

    assert sentiments.count == 1
    assert len(sentiments.results) == 1
    sentiment = sentiments.results[0]
    assert isinstance(sentiment.uuid, UUID)
    assert sentiment.overall_sentiment.label == "positive"
    assert sentiment.overall_sentiment.score == 0.8
    assert len(sentiment.segments) == 1
    assert sentiment.segments[0].text == "We're excited about this partnership"


@pytest.mark.asyncio
async def test_get_sentiment(client, mock_api):
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": meeting_uuid,
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "overall_sentiment": {
            "score": 0.3,
            "label": "neutral",
            "confidence": 0.85,
        },
        "segments": [
            {
                "text": "Let me check the pricing details",
                "start_time": 45.2,
                "end_time": 47.8,
                "speaker": "Alice",
                "sentiment": {
                    "score": 0.3,
                    "label": "neutral",
                    "confidence": 0.92,
                },
            }
        ],
    }

    mock_api.get(
        f"https://api.avoma.com/v1/sentiments/{meeting_uuid}",
        payload=response_data,
    )

    sentiment = await client.sentiments.get(UUID(meeting_uuid))

    assert str(sentiment.uuid) == meeting_uuid
    assert sentiment.overall_sentiment.label == "neutral"
    assert sentiment.overall_sentiment.confidence == 0.85
    assert len(sentiment.segments) == 1
    assert sentiment.segments[0].speaker == "Alice"


@pytest.mark.asyncio
async def test_list_sentiments_by_meeting(client, mock_api):
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "uuid": meeting_uuid,
                "created": "2024-02-14T12:00:00Z",
                "modified": "2024-02-14T12:00:00Z",
                "overall_sentiment": {
                    "score": 0.2,
                    "label": "negative",
                    "confidence": 0.88,
                },
                "segments": [],
            }
        ],
    }

    mock_api.get(
        "https://api.avoma.com/v1/sentiments",
        payload=response_data,
        params={
            "from_date": "2024-02-14T00:00:00Z",
            "to_date": "2024-02-14T23:59:59Z",
            "meeting_uuid": meeting_uuid,
        },
    )

    sentiments = await client.sentiments.list(
        from_date="2024-02-14T00:00:00Z",
        to_date="2024-02-14T23:59:59Z",
        meeting_uuid=UUID(meeting_uuid),
    )

    assert sentiments.count == 1
    assert len(sentiments.results) == 1
    sentiment = sentiments.results[0]
    assert str(sentiment.uuid) == meeting_uuid
    assert sentiment.overall_sentiment.label == "negative"
