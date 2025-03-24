import pytest
from datetime import datetime
from uuid import UUID

from aioresponses import aioresponses
from avoma import AvomaClient
from avoma.models.users import UserCreate, UserUpdate


@pytest.fixture
def client():
    return AvomaClient("test-api-key")


@pytest.fixture
def mock_api():
    with aioresponses() as m:
        yield m


@pytest.mark.asyncio
async def test_list_users(client, mock_api):
    response_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "created": "2024-02-14T12:00:00Z",
                "modified": "2024-02-14T12:00:00Z",
                "role": {
                    "uuid": "123e4567-e89b-12d3-a456-426614174001",
                    "name": "Admin",
                    "permissions": ["read", "write", "admin"],
                },
                "is_active": True,
                "last_login": "2024-02-14T13:00:00Z",
                "timezone": "America/Los_Angeles",
                "department": "Engineering",
                "title": "Senior Engineer",
            }
        ],
    }

    mock_api.get(
        "https://api.avoma.com/v1/users",
        payload=response_data,
    )

    users = await client.users.list()

    assert users.count == 1
    assert len(users.results) == 1
    user = users.results[0]
    assert isinstance(user.uuid, UUID)
    assert user.email == "john.doe@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.role.name == "Admin"
    assert "admin" in user.role.permissions


@pytest.mark.asyncio
async def test_get_user(client, mock_api):
    user_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": user_uuid,
        "email": "jane.smith@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "role": {
            "uuid": "123e4567-e89b-12d3-a456-426614174001",
            "name": "User",
            "permissions": ["read", "write"],
        },
        "is_active": True,
        "timezone": "Europe/London",
    }

    mock_api.get(
        f"https://api.avoma.com/v1/users/{user_uuid}",
        payload=response_data,
    )

    user = await client.users.get(UUID(user_uuid))

    assert str(user.uuid) == user_uuid
    assert user.email == "jane.smith@example.com"
    assert user.role.name == "User"
    assert user.timezone == "Europe/London"


@pytest.mark.asyncio
async def test_create_user(client, mock_api):
    role_uuid = "123e4567-e89b-12d3-a456-426614174001"
    user_data = UserCreate(
        email="new.user@example.com",
        first_name="New",
        last_name="User",
        role_uuid=UUID(role_uuid),
        timezone="Asia/Tokyo",
        department="Sales",
    )

    response_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174002",
        "email": user_data.email,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "role": {
            "uuid": role_uuid,
            "name": "Sales Rep",
            "permissions": ["read", "write"],
        },
        "is_active": True,
        "timezone": user_data.timezone,
        "department": user_data.department,
    }

    mock_api.post(
        "https://api.avoma.com/v1/users",
        payload=response_data,
    )

    user = await client.users.create(user_data)

    assert user.email == user_data.email
    assert user.first_name == user_data.first_name
    assert user.department == user_data.department
    assert str(user.role.uuid) == role_uuid


@pytest.mark.asyncio
async def test_update_user(client, mock_api):
    user_uuid = "123e4567-e89b-12d3-a456-426614174000"
    update_data = UserUpdate(
        first_name="Updated",
        department="Marketing",
        is_active=False,
    )

    response_data = {
        "uuid": user_uuid,
        "email": "existing.user@example.com",
        "first_name": update_data.first_name,
        "last_name": "User",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T13:00:00Z",
        "role": {
            "uuid": "123e4567-e89b-12d3-a456-426614174001",
            "name": "User",
            "permissions": ["read"],
        },
        "is_active": update_data.is_active,
        "department": update_data.department,
    }

    mock_api.put(
        f"https://api.avoma.com/v1/users/{user_uuid}",
        payload=response_data,
    )

    user = await client.users.update(UUID(user_uuid), update_data)

    assert str(user.uuid) == user_uuid
    assert user.first_name == update_data.first_name
    assert user.department == update_data.department
    assert user.is_active == update_data.is_active


@pytest.mark.asyncio
async def test_delete_user(client, mock_api):
    user_uuid = "123e4567-e89b-12d3-a456-426614174000"

    mock_api.delete(
        f"https://api.avoma.com/v1/users/{user_uuid}",
        status=204,
    )

    await client.users.delete(UUID(user_uuid))


@pytest.mark.asyncio
async def test_get_current_user(client, mock_api):
    response_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "email": "current.user@example.com",
        "first_name": "Current",
        "last_name": "User",
        "created": "2024-02-14T12:00:00Z",
        "modified": "2024-02-14T12:00:00Z",
        "role": {
            "uuid": "123e4567-e89b-12d3-a456-426614174001",
            "name": "Admin",
            "permissions": ["read", "write", "admin"],
        },
        "is_active": True,
    }

    mock_api.get(
        "https://api.avoma.com/v1/users/me",
        payload=response_data,
    )

    user = await client.users.get_current()

    assert user.email == "current.user@example.com"
    assert user.role.name == "Admin"
    assert "admin" in user.role.permissions
