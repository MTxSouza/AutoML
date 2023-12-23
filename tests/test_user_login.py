"""
Test user login.
"""
import os
from uuid import uuid4

import pytest

# defining local fixture
random_id = str(uuid4())


@pytest.fixture(scope="function")
def fake_new_user() -> dict:
    return {"username": f"username_{random_id}", "password": f"password_{random_id}"}


def test_create_new_user(fake_new_user, client, base_route):
    """
    insert a new user
    """
    global user_id
    response = client.post(url=os.path.join(base_route, "register"), json=fake_new_user)
    # checking response
    assert response.status_code == 201
    data = response.json()
    user_id = data["id"]
    assert data["username"] == fake_new_user["username"]


def test_login_new_user(fake_new_user, client, base_route):
    """
    Login the new user
    """
    response = client.post(url=os.path.join(base_route, "token"), data=fake_new_user)
    # checking response
    assert response.status_code == 201


def test_delete_new_user(fake_new_user, client, base_route):
    """
    remove new users
    """
    global user_id
    response = client.delete(
        url=os.path.join(base_route, "admin", ""),
        params={"user_id": user_id},
    )
    # checking response
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == fake_new_user["username"]
