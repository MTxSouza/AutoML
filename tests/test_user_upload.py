"""
Test user upload.
"""
import io
import os

import pandas as pd


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
        rdata = response.json()
        for sep in list(rdata["separator"]):
            base_df = pd.read_csv(
                filepath_or_buffer=data["path"], sep=sep, encoding=rdata["encoding"]
            )
            with io.StringIO(initial_value=rdata["file"]) as buffer:
                resp_df = pd.read_csv(
                    filepath_or_buffer=buffer, sep=sep, encoding=rdata["encoding"]
                )
            assert base_df.equals(other=resp_df)


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
    for file_id, _ in enumerate(iterable=valid_files):
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
