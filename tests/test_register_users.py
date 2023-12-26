"""
Test users registration.
"""
import os


def test_create_new_users(fake_new_users, client, base_route):
    """
    insert new users
    """
    for user in fake_new_users:
        response = client.post(url=os.path.join(base_route, "register"), json=user)
        # checking response
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == user["username"]


def test_delete_new_users(fake_new_users, client, base_route):
    """
    remove new users
    """
    for user_id, user in enumerate(iterable=fake_new_users):
        response = client.delete(
            url=os.path.join(base_route, "admin", ""),
            params={"user_id": user_id + 1},
        )
        # checking response
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == user["username"]
