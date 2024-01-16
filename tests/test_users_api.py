import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_create_user(event_loop):
    client = AsyncClient(app=app, base_url="http://test")
    # Test data
    user_data = {
        "name": "John Doe",
        "email": "johnnybhai@example.com",
        "password": "securepassword",
        "is_active": True
    }

    # Make a request to the create_user endpoint
    response = await client.post("/users/", json=user_data)

    # Assertions
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == user_data["name"]
    assert response_data["email"] == user_data["email"]
    # Add more assertions as needed

    await client.aclose()


@pytest.mark.asyncio
async def test_get_user(event_loop):
    client = AsyncClient(app=app, base_url="http://test")

    # Assuming you have a user with a known ID, replace 'some_user_id' with that ID
    user_id = '2389c091-d933-46db-a70a-4e51947ced17'

    response = await client.get(f"/users/{user_id}")

    # Assertions
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == user_id
    # Add more assertions as needed

    await client.aclose()


@pytest.mark.asyncio
async def test_update_user(event_loop):
    client = AsyncClient(app=app, base_url="http://test")

    user_id = '2389c091-d933-46db-a70a-4e51947ced17'  # Replace with a known user ID
    update_data = {
        "name": "Updated Name",
        "email": "updated@example.com",
        # Include other fields you want to update
    }

    response = await client.patch(f"/users/{user_id}", json=update_data)

    # Assertions
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == update_data["name"]
    assert response_data["email"] == update_data["email"]
    # Add more assertions as needed

    await client.aclose()
