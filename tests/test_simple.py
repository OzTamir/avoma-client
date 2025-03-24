import pytest
from unittest.mock import patch, AsyncMock
from uuid import UUID

from avoma import AvomaClient


@pytest.fixture
def client():
    return AvomaClient("test-api-key")


@pytest.mark.asyncio
async def test_simple_mock():
    """Test with a simple mock of the _request method."""
    # Create mock response data
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

    # Create client
    client = AvomaClient("test-api-key")

    # Mock the _request method
    client._request = AsyncMock(return_value=response_data)

    # Call the method that would use _request
    transcriptions = await client.transcriptions.list(
        from_date="2024-02-14T00:00:00Z", to_date="2024-02-14T23:59:59Z"
    )

    # Check that the method was called with the right arguments
    client._request.assert_called_once_with(
        "GET",
        "/transcriptions",
        params={"from_date": "2024-02-14T00:00:00Z", "to_date": "2024-02-14T23:59:59Z"},
    )

    # Check that we got the expected result
    assert len(transcriptions) == 1
    assert transcriptions[0].uuid == UUID("123e4567-e89b-12d3-a456-426614174000")
    assert transcriptions[0].transcript[0].transcript == "Hello, how are you?"
