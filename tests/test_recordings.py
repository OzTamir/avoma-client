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
async def test_get_recording_by_meeting(client, mock_api):
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174001",
        "meeting_uuid": meeting_uuid,
        "audio_url": "https://example.com/audio.mp3",
        "video_url": "https://example.com/video.mp4",
        "valid_till": "2024-02-21T12:00:00Z",
    }

    mock_api.get(
        "https://api.avoma.com/v1/recordings",
        payload=response_data,
        params={"meeting_uuid": meeting_uuid},
    )

    recording = await client.recordings.get_by_meeting(UUID(meeting_uuid))
    assert recording.uuid == UUID("123e4567-e89b-12d3-a456-426614174001")
    assert recording.meeting_uuid == UUID(meeting_uuid)
    assert str(recording.audio_url) == "https://example.com/audio.mp3"
    assert str(recording.video_url) == "https://example.com/video.mp4"


@pytest.mark.asyncio
async def test_get_recording(client, mock_api):
    recording_uuid = "123e4567-e89b-12d3-a456-426614174001"
    response_data = {
        "uuid": recording_uuid,
        "meeting_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "audio_url": "https://example.com/audio.mp3",
        "video_url": "https://example.com/video.mp4",
        "valid_till": "2024-02-21T12:00:00Z",
    }

    mock_api.get(
        f"https://api.avoma.com/v1/recordings/{recording_uuid}", payload=response_data
    )

    recording = await client.recordings.get(UUID(recording_uuid))
    assert recording.uuid == UUID(recording_uuid)
    assert str(recording.audio_url) == "https://example.com/audio.mp3"
    assert str(recording.video_url) == "https://example.com/video.mp4"
