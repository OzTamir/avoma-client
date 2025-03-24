import pytest
from datetime import datetime
from uuid import UUID
import re
import json
from unittest.mock import AsyncMock

from avoma import AvomaClient
from yarl import URL


@pytest.fixture
def client():
    return AvomaClient("test-api-key")


@pytest.mark.asyncio
async def test_list_transcriptions():
    response_data = [
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "transcript": [
                {
                    "transcript": "Hello, how are you?",
                    "timestamps": [0.0, 0.5, 1.0, 1.5],
                    "speaker_id": 1,
                }
            ],
            "speakers": [
                {
                    "email": "speaker@example.com",
                    "id": 1,
                    "is_rep": True,
                    "name": "Test Speaker",
                }
            ],
            "transcription_vtt_url": "https://example.com/transcript.vtt",
        }
    ]

    # Create client and replace _request with mock
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Call the API method
    transcriptions = await client.transcriptions.list(
        from_date="2024-02-14T00:00:00Z", to_date="2024-02-14T23:59:59Z"
    )

    # Verify the mock was called with correct parameters
    client._request.assert_called_once_with(
        "GET",
        "/transcriptions",
        params={"from_date": "2024-02-14T00:00:00Z", "to_date": "2024-02-14T23:59:59Z"},
    )

    # Verify the response was processed correctly
    assert len(transcriptions) == 1
    transcription = transcriptions[0]
    assert transcription.uuid == UUID("123e4567-e89b-12d3-a456-426614174000")
    assert len(transcription.transcript) == 1
    assert transcription.transcript[0].transcript == "Hello, how are you?"
    assert len(transcription.speakers) == 1
    assert transcription.speakers[0].email == "speaker@example.com"
    assert (
        str(transcription.transcription_vtt_url) == "https://example.com/transcript.vtt"
    )


@pytest.mark.asyncio
async def test_list_transcriptions_by_meeting():
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174001"
    response_data = [
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "transcript": [],
            "speakers": [],
            "transcription_vtt_url": "https://example.com/transcript.vtt",
        }
    ]

    # Create client and replace _request with mock
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Call the API method with meeting_uuid
    transcriptions = await client.transcriptions.list(
        from_date="2024-02-14T00:00:00Z",
        to_date="2024-02-14T23:59:59Z",
        meeting_uuid=UUID(meeting_uuid),
    )

    # Verify the mock was called with correct parameters including meeting_uuid
    client._request.assert_called_once_with(
        "GET",
        "/transcriptions",
        params={
            "from_date": "2024-02-14T00:00:00Z",
            "to_date": "2024-02-14T23:59:59Z",
            "meeting_uuid": meeting_uuid,
        },
    )

    # Verify the response
    assert len(transcriptions) == 1
    assert transcriptions[0].uuid == UUID("123e4567-e89b-12d3-a456-426614174000")


@pytest.mark.asyncio
async def test_get_transcription():
    transcription_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": transcription_uuid,
        "transcript": [
            {
                "transcript": "Hello, how are you?",
                "timestamps": [0.0, 0.5, 1.0, 1.5],
                "speaker_id": 1,
            }
        ],
        "speakers": [
            {
                "email": "speaker@example.com",
                "id": 1,
                "is_rep": True,
                "name": "Test Speaker",
            }
        ],
        "transcription_vtt_url": "https://example.com/transcript.vtt",
    }

    # Create client and replace _request with mock
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Call the API method
    transcription = await client.transcriptions.get(UUID(transcription_uuid))

    # Verify the mock was called with correct URL path
    client._request.assert_called_once_with(
        "GET", f"/transcriptions/{transcription_uuid}"
    )

    # Verify the response
    assert transcription.uuid == UUID(transcription_uuid)
    assert len(transcription.transcript) == 1
    assert transcription.transcript[0].transcript == "Hello, how are you?"
    assert len(transcription.speakers) == 1
    assert transcription.speakers[0].email == "speaker@example.com"
