import pytest
from datetime import datetime
from uuid import UUID
from unittest.mock import AsyncMock

from avoma import AvomaClient


@pytest.fixture
def client():
    return AvomaClient("test-api-key")


@pytest.mark.asyncio
async def test_get_recording_by_meeting():
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174001",
        "meeting_uuid": meeting_uuid,
        "audio_url": "https://example.com/audio.mp3",
        "video_url": "https://example.com/video.mp4",
        "valid_till": "2024-02-21T12:00:00Z",
    }

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call
    meeting_id = UUID(meeting_uuid)
    recording = await client.recordings.get_by_meeting(meeting_id)

    # Verify request
    client._request.assert_called_once_with(
        "GET", "/recordings", params={"meeting_uuid": str(meeting_id)}
    )

    # Verify response
    assert recording.uuid == UUID("123e4567-e89b-12d3-a456-426614174001")
    assert recording.meeting_uuid == UUID(meeting_uuid)
    assert str(recording.audio_url) == "https://example.com/audio.mp3"
    assert str(recording.video_url) == "https://example.com/video.mp4"


@pytest.mark.asyncio
async def test_get_recording():
    recording_uuid = "123e4567-e89b-12d3-a456-426614174001"
    response_data = {
        "uuid": recording_uuid,
        "meeting_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "audio_url": "https://example.com/audio.mp3",
        "video_url": "https://example.com/video.mp4",
        "valid_till": "2024-02-21T12:00:00Z",
    }

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call
    recording_id = UUID(recording_uuid)
    recording = await client.recordings.get(recording_id)

    # Verify request
    client._request.assert_called_once_with("GET", f"/recordings/{recording_id}")

    # Verify response
    assert recording.uuid == UUID(recording_uuid)
    assert str(recording.audio_url) == "https://example.com/audio.mp3"
    assert str(recording.video_url) == "https://example.com/video.mp4"
