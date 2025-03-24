import pytest
from datetime import datetime, timedelta
from uuid import UUID
from unittest.mock import AsyncMock

from avoma import AvomaClient
from avoma.models.calls import CallCreate, CallUpdate


@pytest.fixture
def client():
    return AvomaClient("test-api-key")


@pytest.mark.asyncio
async def test_list_calls():
    response_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Weekly Team Sync",
                "description": "Regular team sync meeting",
                "created": "2024-02-14T12:00:00Z",
                "modified": "2024-02-14T12:00:00Z",
                "scheduled_start": "2024-02-15T15:00:00Z",
                "scheduled_duration": 30,
                "status": {
                    "state": "scheduled",
                    "started_at": None,
                    "ended_at": None,
                    "duration": None,
                },
                "participants": [
                    {
                        "uuid": "123e4567-e89b-12d3-a456-426614174001",
                        "email": "participant@example.com",
                        "name": "Team Member",
                        "role": "attendee",
                    }
                ],
                "host": {
                    "uuid": "123e4567-e89b-12d3-a456-426614174002",
                    "email": "host@example.com",
                    "name": "Meeting Host",
                    "role": "host",
                },
                "meeting_url": "https://meet.example.com/123",
                "recording_available": False,
                "transcription_available": False,
                "integration_type": "zoom",
            }
        ],
    }

    # Create client and replace _request with mock
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Call the API method
    from_date = "2024-02-14T00:00:00Z"
    to_date = "2024-02-14T23:59:59Z"
    calls = await client.calls.list(from_date=from_date, to_date=to_date)

    # Verify the mock was called with correct parameters
    client._request.assert_called_once_with(
        "GET", "/calls", params={"from_date": from_date, "to_date": to_date}
    )

    assert calls.count == 1
    assert len(calls.results) == 1
    call = calls.results[0]
    assert isinstance(call.uuid, UUID)
    assert call.title == "Weekly Team Sync"
    assert call.description == "Regular team sync meeting"
    assert call.status.state == "scheduled"
    assert len(call.participants) == 1
    assert call.participants[0].email == "participant@example.com"
    assert call.host.email == "host@example.com"
    assert call.host.role == "host"
    assert call.recording_available is False
    assert call.transcription_available is False


@pytest.mark.asyncio
async def test_get_call():
    call_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": call_uuid,
        "title": "Weekly Team Sync",
        "description": "Regular team sync meeting",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "scheduled_start": "2024-02-15T15:00:00Z",
        "scheduled_duration": 30,
        "status": {
            "state": "scheduled",
            "started_at": None,
            "ended_at": None,
            "duration": None,
        },
        "participants": [
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174001",
                "email": "participant@example.com",
                "name": "Team Member",
                "role": "attendee",
            }
        ],
        "host": {
            "uuid": "123e4567-e89b-12d3-a456-426614174002",
            "email": "host@example.com",
            "name": "Meeting Host",
            "role": "host",
        },
        "meeting_url": "https://meet.example.com/123",
        "recording_available": False,
        "transcription_available": False,
        "integration_type": "zoom",
    }

    # Create client and replace _request with mock
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Call the API method
    call = await client.calls.get(UUID(call_uuid))

    # Verify the mock was called with correct URL path
    client._request.assert_called_once_with("GET", f"/calls/{call_uuid}")

    assert call.uuid == UUID(call_uuid)
    assert call.title == "Weekly Team Sync"
    assert call.description == "Regular team sync meeting"
    assert call.status.state == "scheduled"
    assert len(call.participants) == 1
    assert call.participants[0].email == "participant@example.com"
    assert call.host.email == "host@example.com"
    assert call.host.role == "host"
    assert call.recording_available is False
    assert call.transcription_available is False


@pytest.mark.asyncio
async def test_create_call():
    response_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "title": "New Call",
        "description": "Created via API",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "scheduled_start": "2024-02-15T15:00:00Z",
        "scheduled_duration": 45,
        "status": {
            "state": "scheduled",
            "started_at": None,
            "ended_at": None,
            "duration": None,
        },
        "participants": [
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174001",
                "email": "participant@example.com",
                "name": "Team Member",
                "role": "attendee",
            }
        ],
        "host": {
            "uuid": "123e4567-e89b-12d3-a456-426614174002",
            "email": "host@example.com",
            "name": "Meeting Host",
            "role": "host",
        },
        "meeting_url": "https://meet.example.com/new",
        "recording_available": False,
        "transcription_available": False,
        "integration_type": "zoom",
    }

    scheduled_start = datetime.now() + timedelta(days=1)
    call_data = CallCreate(
        title="New Call",
        description="Created via API",
        scheduled_start=scheduled_start.isoformat(),
        scheduled_duration=45,
        host_email="host@example.com",
        participant_emails=["participant@example.com"],
        integration_type="zoom",
    )

    # Create client and replace _request with mock
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Call the API method
    call = await client.calls.create(call_data)

    # Verify the mock was called with correct parameters
    client._request.assert_called_once_with(
        "POST", "/calls", json=call_data.model_dump(exclude_unset=True)
    )

    assert call.uuid == UUID("123e4567-e89b-12d3-a456-426614174000")
    assert call.title == "New Call"
    assert call.description == "Created via API"
    assert call.scheduled_duration == 45
    assert call.recording_available is False
    assert call.transcription_available is False


@pytest.mark.asyncio
async def test_update_call():
    call_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": call_uuid,
        "title": "Updated Call",
        "description": "Updated via API",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T13:00:00Z",
        "scheduled_start": "2024-02-15T16:00:00Z",
        "scheduled_duration": 60,
        "status": {
            "state": "scheduled",
            "started_at": None,
            "ended_at": None,
            "duration": None,
        },
        "participants": [],
        "host": {
            "uuid": "123e4567-e89b-12d3-a456-426614174002",
            "email": "host@example.com",
            "name": "Meeting Host",
            "role": "host",
        },
        "meeting_url": "https://meet.example.com/updated",
        "recording_available": False,
        "transcription_available": False,
        "integration_type": "teams",
    }

    update_data = CallUpdate(
        title="Updated Call",
        description="Updated via API",
        scheduled_duration=60,
    )

    # Create client and replace _request with mock
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Call the API method
    call = await client.calls.update(UUID(call_uuid), update_data)

    # Verify the mock was called with correct parameters
    client._request.assert_called_once_with(
        "PUT", f"/calls/{call_uuid}", json=update_data.model_dump(exclude_unset=True)
    )

    assert call.uuid == UUID(call_uuid)
    assert call.title == "Updated Call"
    assert call.description == "Updated via API"
    assert call.scheduled_duration == 60
    assert call.recording_available is False
    assert call.transcription_available is False


@pytest.mark.asyncio
async def test_call_lifecycle():
    call_uuid = "123e4567-e89b-12d3-a456-426614174000"

    # Base call response with required fields
    base_call = {
        "uuid": call_uuid,
        "title": "Test Call",
        "description": "Lifecycle test",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "scheduled_start": "2024-02-14T15:00:00Z",
        "scheduled_duration": 30,
        "participants": [],
        "host": {
            "uuid": "123e4567-e89b-12d3-a456-426614174002",
            "email": "host@example.com",
            "name": "Meeting Host",
            "role": "host",
        },
        "meeting_url": "https://meet.example.com/test",
        "recording_available": False,
        "transcription_available": False,
    }

    # Mock for start
    start_response = {
        **base_call,
        "status": {
            "state": "in_progress",
            "started_at": "2024-02-14T15:00:00Z",
            "ended_at": None,
            "duration": None,
        },
    }

    # Mock for end
    end_response = {
        **base_call,
        "status": {
            "state": "completed",
            "started_at": "2024-02-14T15:00:00Z",
            "ended_at": "2024-02-14T15:30:00Z",
            "duration": 1800,  # 30 minutes in seconds
        },
        "recording_available": True,
    }

    # Mock for cancel
    cancel_response = {
        **base_call,
        "status": {
            "state": "cancelled",
            "started_at": None,
            "ended_at": None,
            "duration": None,
        },
    }

    # Create client and replace _request with multiple return values
    client = AvomaClient("test-api-key")
    mock_request = AsyncMock()
    mock_request.side_effect = [start_response, end_response, cancel_response]
    client._request = mock_request

    # Test start method
    start_result = await client.calls.start(UUID(call_uuid))
    assert start_result.status.state == "in_progress"
    assert (
        start_result.status.started_at.isoformat().replace("+00:00", "Z")
        == "2024-02-14T15:00:00Z"
    )

    # Test end method
    end_result = await client.calls.end(UUID(call_uuid))
    assert end_result.status.state == "completed"
    assert (
        end_result.status.ended_at.isoformat().replace("+00:00", "Z")
        == "2024-02-14T15:30:00Z"
    )
    assert end_result.status.duration == 1800

    # Test cancel method
    cancel_result = await client.calls.cancel(UUID(call_uuid))
    assert cancel_result.status.state == "cancelled"

    # Verify the mock was called with correct parameters
    assert mock_request.call_count == 3
    mock_request.assert_any_call("POST", f"/calls/{call_uuid}/start")
    mock_request.assert_any_call("POST", f"/calls/{call_uuid}/end")
    mock_request.assert_any_call("POST", f"/calls/{call_uuid}/cancel")
