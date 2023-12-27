"""
Test user upload.
"""
import os


def test_upload_valid_files(token, fake_new_user, valid_files, client, base_route):
    """
    Upload a list of files
    """
    # uploading files
    for data in valid_files:
        ext = data["path"].split(".")[-1].lower()
        with open(file=data["path"], mode="rb") as file_buffer:
            response = client.post(
                url=os.path.join(base_route, "users", "upload"),
                files={"file": (file_buffer.name, file_buffer, f"application/{ext}")},
                data=fake_new_user,
                headers=token,
            )
        # checking response
        assert response.status_code == data["status"]


def test_upload_invalid_files(token, fake_new_user, invalid_files, client, base_route):
    """
    Upload a list of files
    """
    # uploading files
    for data in invalid_files:
        ext = data["path"].split(".")[-1].lower()
        with open(file=data["path"], mode="rb") as file_buffer:
            response = client.post(
                url=os.path.join(base_route, "users", "upload"),
                files={"file": (file_buffer.name, file_buffer, f"application/{ext}")},
                data=fake_new_user,
                headers=token,
            )
        # checking response
        assert response.status_code == data["status"]


def test_delete_files(token, valid_files, client, base_route):
    """
    Delete a list of files
    """
    # deleting files
    for file_id, data in enumerate(iterable=valid_files):
        response = client.delete(
            url=os.path.join(base_route, "users", "files"),
            params={"file_id": file_id + 1},
            headers=token,
        )
        # checking response
        assert response.status_code == 201


def test_delete_new_user(fake_new_user, client, base_route):
    """
    remove new users
    """
    response = client.delete(
        url=os.path.join(base_route, "admin", ""),
        params={"user_id": 1},
    )
    # checking response
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == fake_new_user["username"]
