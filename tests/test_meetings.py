import pytest
from datetime import datetime, timezone
from uuid import UUID
from unittest.mock import AsyncMock

from avoma import AvomaClient


@pytest.fixture
def client():
    return AvomaClient("test-api-key")


@pytest.mark.asyncio
async def test_list_meetings():
    # Mock response data for first page
    first_page_data = {
        "count": 2,
        "next": "https://api.avoma.com/v1/meetings/?page=2",
        "previous": None,
        "results": [
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "subject": "Test Meeting 1",
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

    # Mock response data for second page
    second_page_data = {
        "count": 2,
        "next": None,
        "previous": "https://api.avoma.com/v1/meetings/?page=1",
        "results": [
            {
                "uuid": "223e4567-e89b-12d3-a456-426614174000",
                "subject": "Test Meeting 2",
                "created": "2024-02-14T13:00:00Z",
                "modified": "2024-02-14T13:00:00Z",
                "is_private": False,
                "is_internal": True,
                "organizer_email": "test2@example.com",
                "state": "completed",
                "attendees": [],
                "audio_ready": True,
                "video_ready": True,
                "is_call": False,
                "notes_ready": True,
                "transcript_ready": True,
            }
        ],
    }

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    mock_request = AsyncMock()
    mock_request.side_effect = [first_page_data, second_page_data]
    client._request = mock_request

    # Test without pagination
    from_date = "2024-02-14T00:00:00Z"
    to_date = "2024-02-14T23:59:59Z"
    meetings = await client.meetings.list(from_date=from_date, to_date=to_date)

    # Verify single page request
    mock_request.assert_called_once_with(
        "GET",
        "meetings",
        params={
            "from_date": from_date,
            "to_date": to_date,
            "page_size": 100,  # Default page size should be included
        },
    )

    # Verify first page response
    assert meetings.count == 2
    assert meetings.next == "https://api.avoma.com/v1/meetings/?page=2"
    assert meetings.previous is None
    assert len(meetings.results) == 1
    assert meetings.results[0].subject == "Test Meeting 1"

    # Reset mock
    mock_request.reset_mock()
    mock_request.side_effect = [first_page_data, second_page_data]

    # Test with pagination
    meetings = await client.meetings.list(
        from_date=from_date,
        to_date=to_date,
        follow_pagination=True,
    )

    # Verify both pages were requested
    assert mock_request.call_count == 2
    mock_request.assert_any_call(
        "GET",
        "meetings",
        params={
            "from_date": from_date,
            "to_date": to_date,
            "page_size": 100,  # Default page size should be included
        },
    )
    mock_request.assert_any_call(
        "GET", "", full_url="https://api.avoma.com/v1/meetings/?page=2"
    )

    # Verify combined response
    assert meetings.count == 2
    assert meetings.next is None
    assert meetings.previous is None
    assert len(meetings.results) == 2
    assert meetings.results[0].subject == "Test Meeting 1"
    assert meetings.results[1].subject == "Test Meeting 2"


@pytest.mark.asyncio
async def test_get_meeting():
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

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call
    meeting = await client.meetings.get(UUID(meeting_uuid))

    # Verify the request was made with correct path
    client._request.assert_called_once_with("GET", f"meetings/{meeting_uuid}")

    # Verify response
    assert meeting.uuid == UUID(meeting_uuid)
    assert meeting.subject == "Test Meeting"
    assert meeting.state == "completed"


@pytest.mark.asyncio
async def test_get_meeting_insights():
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

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call
    insights = await client.meetings.get_insights(UUID(meeting_uuid))

    # Verify the request was made with correct path
    client._request.assert_called_once_with("GET", f"meetings/{meeting_uuid}/insights")

    # Verify response
    assert len(insights.ai_notes) == 1
    assert insights.ai_notes[0].note_type == "action_item"
    assert len(insights.speakers) == 1
    assert insights.speakers[0].email == "speaker@example.com"


@pytest.mark.asyncio
async def test_get_meeting_sentiments():
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "sentiment": 1,
        "sentiment_ranges": [{"score": 0.8, "time_range": [0.0, 10.0]}],
    }

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call
    sentiments = await client.meetings.get_sentiments(UUID(meeting_uuid))

    # Verify the request was made with correct parameters
    client._request.assert_called_once_with(
        "GET", "meeting_sentiments", params={"uuid": str(meeting_uuid)}
    )

    # Verify response
    assert sentiments.sentiment == 1
    assert len(sentiments.sentiment_ranges) == 1
    assert sentiments.sentiment_ranges[0].score == 0.8
