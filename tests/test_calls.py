import pytest
from datetime import datetime, timedelta
from uuid import UUID

from aioresponses import aioresponses
from avoma import AvomaClient
from avoma.models.calls import CallCreate, CallUpdate


@pytest.fixture
def client():
    return AvomaClient("test-api-key")


@pytest.fixture
def mock_api():
    with aioresponses() as m:
        yield m


@pytest.mark.asyncio
async def test_list_calls(client, mock_api):
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

    mock_api.get(
        "https://api.avoma.com/v1/calls",
        payload=response_data,
        params={
            "from_date": "2024-02-14T00:00:00Z",
            "to_date": "2024-02-14T23:59:59Z",
        },
    )

    calls = await client.calls.list(
        from_date="2024-02-14T00:00:00Z", to_date="2024-02-14T23:59:59Z"
    )

    assert calls.count == 1
    assert len(calls.results) == 1
    call = calls.results[0]
    assert isinstance(call.uuid, UUID)
    assert call.title == "Weekly Team Sync"
    assert call.status.state == "scheduled"
    assert len(call.participants) == 1
    assert call.host.email == "host@example.com"


@pytest.mark.asyncio
async def test_get_call(client, mock_api):
    call_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": call_uuid,
        "title": "Sales Demo",
        "description": "Product demo for potential client",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "scheduled_start": "2024-02-15T14:00:00Z",
        "scheduled_duration": 60,
        "status": {
            "state": "completed",
            "started_at": "2024-02-15T14:00:00Z",
            "ended_at": "2024-02-15T15:00:00Z",
            "duration": 3600,
        },
        "participants": [],
        "host": {
            "uuid": "123e4567-e89b-12d3-a456-426614174001",
            "email": "sales@example.com",
            "name": "Sales Rep",
            "role": "host",
        },
        "recording_available": True,
        "transcription_available": True,
    }

    mock_api.get(
        f"https://api.avoma.com/v1/calls/{call_uuid}",
        payload=response_data,
    )

    call = await client.calls.get(UUID(call_uuid))

    assert str(call.uuid) == call_uuid
    assert call.title == "Sales Demo"
    assert call.status.state == "completed"
    assert call.status.duration == 3600
    assert call.recording_available
    assert call.transcription_available


@pytest.mark.asyncio
async def test_create_call(client, mock_api):
    scheduled_start = datetime.utcnow() + timedelta(days=1)
    call_data = CallCreate(
        title="Project Kickoff",
        description="Initial project planning meeting",
        scheduled_start=scheduled_start,
        scheduled_duration=45,
        host_email="project.lead@example.com",
        participant_emails=["team1@example.com", "team2@example.com"],
        integration_type="teams",
    )

    response_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "title": call_data.title,
        "description": call_data.description,
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "scheduled_start": scheduled_start.isoformat() + "Z",
        "scheduled_duration": call_data.scheduled_duration,
        "status": {"state": "scheduled"},
        "participants": [
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174001",
                "email": email,
                "name": "Team Member",
                "role": "attendee",
            }
            for email in call_data.participant_emails
        ],
        "host": {
            "uuid": "123e4567-e89b-12d3-a456-426614174002",
            "email": call_data.host_email,
            "name": "Project Lead",
            "role": "host",
        },
        "integration_type": call_data.integration_type,
        "recording_available": False,
        "transcription_available": False,
    }

    mock_api.post(
        "https://api.avoma.com/v1/calls",
        payload=response_data,
    )

    call = await client.calls.create(call_data)

    assert call.title == call_data.title
    assert call.scheduled_duration == call_data.scheduled_duration
    assert call.host.email == call_data.host_email
    assert len(call.participants) == len(call_data.participant_emails)


@pytest.mark.asyncio
async def test_update_call(client, mock_api):
    call_uuid = "123e4567-e89b-12d3-a456-426614174000"
    update_data = CallUpdate(
        title="Updated Meeting Title",
        description="Updated agenda",
        participant_emails=["new.participant@example.com"],
    )

    response_data = {
        "uuid": call_uuid,
        "title": update_data.title,
        "description": update_data.description,
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T13:00:00Z",
        "scheduled_start": "2024-02-15T15:00:00Z",
        "scheduled_duration": 30,
        "status": {"state": "scheduled"},
        "participants": [
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174001",
                "email": "new.participant@example.com",
                "name": "New Participant",
                "role": "attendee",
            }
        ],
        "host": {
            "uuid": "123e4567-e89b-12d3-a456-426614174002",
            "email": "host@example.com",
            "name": "Host",
            "role": "host",
        },
        "recording_available": False,
        "transcription_available": False,
    }

    mock_api.put(
        f"https://api.avoma.com/v1/calls/{call_uuid}",
        payload=response_data,
    )

    call = await client.calls.update(UUID(call_uuid), update_data)

    assert str(call.uuid) == call_uuid
    assert call.title == update_data.title
    assert call.description == update_data.description
    assert len(call.participants) == 1
    assert call.participants[0].email == "new.participant@example.com"


@pytest.mark.asyncio
async def test_call_lifecycle(client, mock_api):
    call_uuid = "123e4567-e89b-12d3-a456-426614174000"
    base_response = {
        "uuid": call_uuid,
        "title": "Test Call",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "scheduled_start": "2024-02-14T15:00:00Z",
        "scheduled_duration": 30,
        "participants": [],
        "host": {
            "uuid": "123e4567-e89b-12d3-a456-426614174001",
            "email": "host@example.com",
            "name": "Host",
            "role": "host",
        },
        "recording_available": False,
        "transcription_available": False,
    }

    # Test starting a call
    start_response = {
        **base_response,
        "status": {
            "state": "in_progress",
            "started_at": "2024-02-14T15:00:00Z",
            "ended_at": None,
            "duration": None,
        },
    }
    mock_api.post(
        f"https://api.avoma.com/v1/calls/{call_uuid}/start",
        payload=start_response,
    )

    started_call = await client.calls.start(UUID(call_uuid))
    assert started_call.status.state == "in_progress"
    assert started_call.status.started_at is not None

    # Test ending a call
    end_response = {
        **base_response,
        "status": {
            "state": "completed",
            "started_at": "2024-02-14T15:00:00Z",
            "ended_at": "2024-02-14T15:30:00Z",
            "duration": 1800,
        },
    }
    mock_api.post(
        f"https://api.avoma.com/v1/calls/{call_uuid}/end",
        payload=end_response,
    )

    ended_call = await client.calls.end(UUID(call_uuid))
    assert ended_call.status.state == "completed"
    assert ended_call.status.duration == 1800

    # Test cancelling a call
    cancel_response = {
        **base_response,
        "status": {
            "state": "cancelled",
            "started_at": None,
            "ended_at": None,
            "duration": None,
        },
    }
    mock_api.post(
        f"https://api.avoma.com/v1/calls/{call_uuid}/cancel",
        payload=cancel_response,
    )

    cancelled_call = await client.calls.cancel(UUID(call_uuid))
    assert cancelled_call.status.state == "cancelled"
