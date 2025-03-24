import pytest
from datetime import datetime
from uuid import UUID
from unittest.mock import AsyncMock

from avoma import AvomaClient


@pytest.fixture
def client():
    return AvomaClient("test-api-key")


@pytest.mark.asyncio
async def test_list_notes_json():
    response_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "created": "2024-02-14T12:00:00Z",
                "modified": "2024-02-14T12:00:00Z",
                "data": {
                    "sections": [
                        {
                            "title": "Action Items",
                            "items": ["Schedule follow-up", "Send documentation"],
                        }
                    ]
                },
            }
        ],
    }

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call with the default output_format=json
    from_date = "2024-02-14T00:00:00Z"
    to_date = "2024-02-14T23:59:59Z"
    notes = await client.notes.list(from_date=from_date, to_date=to_date)

    # Verify request
    client._request.assert_called_once_with(
        "GET",
        "/notes",
        params={"from_date": from_date, "to_date": to_date, "output_format": "json"},
    )

    # Verify response
    assert notes.count == 1
    assert len(notes.results) == 1
    note = notes.results[0]
    assert isinstance(note.data, dict)
    assert "sections" in note.data
    assert len(note.data["sections"]) == 1


@pytest.mark.asyncio
async def test_list_notes_markdown():
    response_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "created": "2024-02-14T12:00:00Z",
                "modified": "2024-02-14T12:00:00Z",
                "data": "# Action Items\n\n- Schedule follow-up\n- Send documentation",
            }
        ],
    }

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call with output_format=markdown
    from_date = "2024-02-14T00:00:00Z"
    to_date = "2024-02-14T23:59:59Z"
    output_format = "markdown"
    notes = await client.notes.list(
        from_date=from_date, to_date=to_date, output_format=output_format
    )

    # Verify request
    client._request.assert_called_once_with(
        "GET",
        "/notes",
        params={
            "from_date": from_date,
            "to_date": to_date,
            "output_format": output_format,
        },
    )

    # Verify response
    assert notes.count == 1
    assert len(notes.results) == 1
    note = notes.results[0]
    assert isinstance(note.data, str)
    assert "# Action Items" in note.data


@pytest.mark.asyncio
async def test_list_notes_by_meeting():
    meeting_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "created": "2024-02-14T12:00:00Z",
                "modified": "2024-02-14T12:00:00Z",
                "data": {},
            }
        ],
    }

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call with meeting_uuid
    from_date = "2024-02-14T00:00:00Z"
    to_date = "2024-02-14T23:59:59Z"
    meeting_id = UUID(meeting_uuid)
    notes = await client.notes.list(
        from_date=from_date, to_date=to_date, meeting_uuid=meeting_id
    )

    # Verify request with the actual UUID objects
    client._request.assert_called_once_with(
        "GET",
        "/notes",
        params={
            "from_date": from_date,
            "to_date": to_date,
            "meeting_uuid": meeting_id,
            "output_format": "json",
        },
    )

    # Verify response
    assert notes.count == 1
    assert len(notes.results) == 1


@pytest.mark.asyncio
async def test_list_notes_by_category():
    category_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "created": "2024-02-14T12:00:00Z",
                "modified": "2024-02-14T12:00:00Z",
                "data": {},
            }
        ],
    }

    # Create client and mock _request method
    client = AvomaClient("test-api-key")
    client._request = AsyncMock(return_value=response_data)

    # Make the API call with custom_category
    from_date = "2024-02-14T00:00:00Z"
    to_date = "2024-02-14T23:59:59Z"
    category_id = UUID(category_uuid)
    notes = await client.notes.list(
        from_date=from_date, to_date=to_date, custom_category=category_id
    )

    # Verify request with the actual UUID objects
    client._request.assert_called_once_with(
        "GET",
        "/notes",
        params={
            "from_date": from_date,
            "to_date": to_date,
            "custom_category": category_id,
            "output_format": "json",
        },
    )

    # Verify response
    assert notes.count == 1
    assert len(notes.results) == 1
