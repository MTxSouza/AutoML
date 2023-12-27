"""
Script that contains all init configuration
and variables that will be used during test.
"""
import os
import sys

sys.path.append(os.getcwd())

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from server.app import app
from server.database.config import Base, create_engine, sessionmaker
from server.database.utils import get_db

# creating testing database
folder_path = os.path.join(os.getcwd(), "tests")
engine = create_engine(
    url=os.path.join(f"sqlite+pysqlite:///{folder_path}", "db.sqlite3"),
    echo=False,
)
TestingSession = sessionmaker(bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSession()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# creating fixures
@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app=app)


@pytest.fixture(scope="session")
def base_route() -> str:
    return "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def fake_new_users() -> list[dict]:
    return [
        {"username": f"user_{str(uuid4())}_{i}", "password": str(uuid4())}
        for i in range(10)
    ]


@pytest.fixture(scope="session")
def datasets() -> list[dict]:
    return [
        {"path": os.path.join(folder_path, "data", "anv.csv"), "status_insert": 201, "status_delete": 201},
        {"path": os.path.join(folder_path, "data", "books.csv"), "status_insert": 201, "status_delete": 201},
        {"path": os.path.join(folder_path, "data", "heart.csv"), "status_insert": 201, "status_delete": 201},
        {"path": os.path.join(folder_path, "data", "netflix.csv"), "status_insert": 201, "status_delete": 201},
        {"path": os.path.join(folder_path, "data", "tweets.csv"), "status_insert": 413, "status_delete": 404},
    ]
    
@pytest.fixture(scope="session")
def fake_new_user() -> dict:
    return {"username": f"username_{str(uuid4())}", "password": f"password_{str(uuid4())}"}

@pytest.fixture(scope="session")
def token(fake_new_user, client, base_route):
    """
    Login the new user
    """
    # register
    response = client.post(url=os.path.join(base_route, "register"), json=fake_new_user)
    # checking response
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == fake_new_user["username"]
    # login
    response = client.post(url=os.path.join(base_route, "token"), data=fake_new_user)
    # checking response
    assert response.status_code == 201
    return {"Authorization": f"Bearer {response.json().get('access_token')}"}