import pytest
from datetime import datetime, timezone
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
async def test_list_meetings(client, mock_api):
    # Mock response data
    response_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "subject": "Test Meeting",
                "created": "2024-02-14T12:00:00Z",
                "modified": "2024-02-14T12:00:00Z",
                "is_private": False,
                "is_internal": True,
                "organizer_email": "test@example.com",
                "state": "completed",
                "attendees": [
                    {
                        "email": "attendee@example.com",
                        "name": "Test Attendee",
                        "response_status": "accepted",
                        "uuid": "123e4567-e89b-12d3-a456-426614174001",
                    }
                ],
                "audio_ready": True,
                "video_ready": True,
                "is_call": False,
                "notes_ready": True,
                "transcript_ready": True,
            }
        ],
    }

    # Mock the API call
    mock_api.get(
        "https://api.avoma.com/v1/meetings?from_date=2024-02-14T00%3A00%3A00Z&to_date=2024-02-14T23%3A59%3A59Z",
        payload=response_data,
    )

    # Make the API call
    meetings = await client.meetings.list(
        from_date="2024-02-14T00:00:00Z", to_date="2024-02-14T23:59:59Z"
    )

    # Verify response
    assert meetings.count == 1
    assert meetings.next is None
    assert meetings.previous is None
    assert len(meetings.results) == 1

    meeting = meetings.results[0]
    assert meeting.uuid == UUID("123e4567-e89b-12d3-a456-426614174000")
    assert meeting.subject == "Test Meeting"
    assert meeting.is_internal is True
    assert len(meeting.attendees) == 1
    assert meeting.attendees[0].email == "attendee@example.com"


@pytest.mark.asyncio
async def test_get_meeting(client, mock_api):
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": meeting_uuid,
        "subject": "Test Meeting",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "is_private": False,
        "is_internal": True,
        "organizer_email": "test@example.com",
        "state": "completed",
        "attendees": [],
        "audio_ready": True,
        "video_ready": True,
        "is_call": False,
        "notes_ready": True,
        "transcript_ready": True,
    }

    mock_api.get(
        f"https://api.avoma.com/v1/meetings/{meeting_uuid}", payload=response_data
    )

    meeting = await client.meetings.get(UUID(meeting_uuid))
    assert meeting.uuid == UUID(meeting_uuid)
    assert meeting.subject == "Test Meeting"
    assert meeting.state == "completed"


@pytest.mark.asyncio
async def test_get_meeting_insights(client, mock_api):
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "ai_notes": [
            {
                "note_type": "action_item",
                "uuid": "123e4567-e89b-12d3-a456-426614174002",
                "start": 10.5,
                "end": 15.2,
                "text": "Schedule follow-up meeting",
                "speaker_id": 1,
            }
        ],
        "keywords": {},
        "speakers": [
            {
                "email": "speaker@example.com",
                "id": 1,
                "is_rep": True,
                "name": "Test Speaker",
            }
        ],
    }

    mock_api.get(
        f"https://api.avoma.com/v1/meetings/{meeting_uuid}/insights",
        payload=response_data,
    )

    insights = await client.meetings.get_insights(UUID(meeting_uuid))
    assert len(insights.ai_notes) == 1
    assert insights.ai_notes[0].note_type == "action_item"
    assert len(insights.speakers) == 1
    assert insights.speakers[0].email == "speaker@example.com"


@pytest.mark.asyncio
async def test_get_meeting_sentiments(client, mock_api):
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "sentiment": 1,
        "sentiment_ranges": [{"score": 0.8, "time_range": [0.0, 10.0]}],
    }

    mock_api.get(
        "https://api.avoma.com/v1/meeting_sentiments",
        payload=response_data,
        params={"uuid": meeting_uuid},
    )

    sentiments = await client.meetings.get_sentiments(UUID(meeting_uuid))
    assert sentiments.sentiment == 1
    assert len(sentiments.sentiment_ranges) == 1
    assert sentiments.sentiment_ranges[0].score == 0.8
