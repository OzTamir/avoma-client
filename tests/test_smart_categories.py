import pytest
from datetime import datetime
from uuid import UUID

from aioresponses import aioresponses
from avoma import AvomaClient
from avoma.models.smart_categories import SmartCategoryCreate, SmartCategoryUpdate


@pytest.fixture
def client():
    return AvomaClient("test-api-key")


@pytest.fixture
def mock_api():
    with aioresponses() as m:
        yield m


@pytest.mark.asyncio
async def test_list_smart_categories(client, mock_api):
    response_data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Test Category",
                "key": "test_category",
                "is_default": False,
                "keywords": [
                    {
                        "created": "2024-02-14T12:00:00Z",
                        "custom_category": "123e4567-e89b-12d3-a456-426614174000",
                        "is_primary": True,
                        "label": "Test Keyword",
                        "uuid": "123e4567-e89b-12d3-a456-426614174001",
                        "variations": ["test", "testing"],
                    }
                ],
                "prompts": [
                    {
                        "created": "2024-02-14T12:00:00Z",
                        "custom_category": "123e4567-e89b-12d3-a456-426614174000",
                        "label": "Test Prompt",
                        "uuid": "123e4567-e89b-12d3-a456-426614174002",
                        "variations": ["what is the test?", "how does it test?"],
                    }
                ],
                "settings": {
                    "aug_notes_enabled": True,
                    "keyword_notes_enabled": True,
                    "keyword_tracking_enabled": True,
                    "prompt_extract_length": "medium",
                    "prompt_extract_strategy": "after",
                    "prompt_notes_enabled": True,
                },
            }
        ],
    }

    mock_api.get("https://api.avoma.com/v1/smart_categories", payload=response_data)

    categories = await client.smart_categories.list()
    assert len(categories) == 1

    category = categories[0]
    assert category.uuid == UUID("123e4567-e89b-12d3-a456-426614174000")
    assert category.name == "Test Category"
    assert len(category.keywords) == 1
    assert len(category.prompts) == 1
    assert category.settings.aug_notes_enabled is True


@pytest.mark.asyncio
async def test_get_smart_category(client, mock_api):
    category_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response_data = {
        "uuid": category_uuid,
        "name": "Test Category",
        "key": "test_category",
        "is_default": False,
        "keywords": [],
        "prompts": [],
        "settings": {
            "aug_notes_enabled": True,
            "keyword_notes_enabled": True,
            "keyword_tracking_enabled": True,
            "prompt_extract_length": "medium",
            "prompt_extract_strategy": "after",
            "prompt_notes_enabled": True,
        },
    }

    mock_api.get(
        f"https://api.avoma.com/v1/smart_categories/{category_uuid}",
        payload=response_data,
    )

    category = await client.smart_categories.get(UUID(category_uuid))
    assert category.uuid == UUID(category_uuid)
    assert category.name == "Test Category"
    assert category.settings.prompt_extract_length == "medium"


@pytest.mark.asyncio
async def test_create_smart_category(client, mock_api):
    new_category = SmartCategoryCreate(
        name="New Category",
        keywords=["keyword1", "keyword2"],
        prompts=["prompt1", "prompt2"],
        settings={
            "aug_notes_enabled": True,
            "keyword_notes_enabled": True,
            "keyword_tracking_enabled": True,
            "prompt_extract_length": "medium",
            "prompt_extract_strategy": "after",
            "prompt_notes_enabled": True,
        },
    )

    response_data = {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "name": "New Category",
        "key": "new_category",
        "is_default": False,
        "keywords": [],
        "prompts": [],
        "settings": new_category.settings.model_dump(),
    }

    mock_api.post("https://api.avoma.com/v1/smart_categories", payload=response_data)

    category = await client.smart_categories.create(new_category)
    assert category.name == "New Category"
    assert category.settings.prompt_extract_length == "medium"


@pytest.mark.asyncio
async def test_update_smart_category(client, mock_api):
    category_uuid = "123e4567-e89b-12d3-a456-426614174000"
    update_data = SmartCategoryUpdate(
        keywords=["updated_keyword"],
        prompts=["updated_prompt"],
        settings={
            "aug_notes_enabled": False,
            "keyword_notes_enabled": True,
            "keyword_tracking_enabled": True,
            "prompt_extract_length": "short",
            "prompt_extract_strategy": "before",
            "prompt_notes_enabled": True,
        },
    )

    response_data = {
        "uuid": category_uuid,
        "name": "Test Category",
        "key": "test_category",
        "is_default": False,
        "keywords": [],
        "prompts": [],
        "settings": update_data.settings.model_dump(),
    }

    mock_api.patch(
        f"https://api.avoma.com/v1/smart_categories/{category_uuid}",
        payload=response_data,
    )

    category = await client.smart_categories.update(UUID(category_uuid), update_data)
    assert category.uuid == UUID(category_uuid)
    assert category.settings.prompt_extract_length == "short"
    assert category.settings.aug_notes_enabled is False
