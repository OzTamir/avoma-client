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
async def test_list_notes_json(client, mock_api):
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

    mock_api.get(
        "https://api.avoma.com/v1/notes",
        payload=response_data,
        params={
            "from_date": "2024-02-14T00:00:00Z",
            "to_date": "2024-02-14T23:59:59Z",
            "output_format": "json",
        },
    )

    notes = await client.notes.list(
        from_date="2024-02-14T00:00:00Z", to_date="2024-02-14T23:59:59Z"
    )

    assert notes.count == 1
    assert len(notes.results) == 1
    note = notes.results[0]
    assert isinstance(note.data, dict)
    assert "sections" in note.data
    assert len(note.data["sections"]) == 1


@pytest.mark.asyncio
async def test_list_notes_markdown(client, mock_api):
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

    mock_api.get(
        "https://api.avoma.com/v1/notes",
        payload=response_data,
        params={
            "from_date": "2024-02-14T00:00:00Z",
            "to_date": "2024-02-14T23:59:59Z",
            "output_format": "markdown",
        },
    )

    notes = await client.notes.list(
        from_date="2024-02-14T00:00:00Z",
        to_date="2024-02-14T23:59:59Z",
        output_format="markdown",
    )

    assert notes.count == 1
    assert len(notes.results) == 1
    note = notes.results[0]
    assert isinstance(note.data, str)
    assert "# Action Items" in note.data


@pytest.mark.asyncio
async def test_list_notes_by_meeting(client, mock_api):
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

    mock_api.get(
        "https://api.avoma.com/v1/notes",
        payload=response_data,
        params={
            "from_date": "2024-02-14T00:00:00Z",
            "to_date": "2024-02-14T23:59:59Z",
            "meeting_uuid": meeting_uuid,
            "output_format": "json",
        },
    )

    notes = await client.notes.list(
        from_date="2024-02-14T00:00:00Z",
        to_date="2024-02-14T23:59:59Z",
        meeting_uuid=UUID(meeting_uuid),
    )

    assert notes.count == 1
    assert len(notes.results) == 1


@pytest.mark.asyncio
async def test_list_notes_by_category(client, mock_api):
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

    mock_api.get(
        "https://api.avoma.com/v1/notes",
        payload=response_data,
        params={
            "from_date": "2024-02-14T00:00:00Z",
            "to_date": "2024-02-14T23:59:59Z",
            "custom_category": category_uuid,
            "output_format": "json",
        },
    )

    notes = await client.notes.list(
        from_date="2024-02-14T00:00:00Z",
        to_date="2024-02-14T23:59:59Z",
        custom_category=UUID(category_uuid),
    )

    assert notes.count == 1
    assert len(notes.results) == 1
