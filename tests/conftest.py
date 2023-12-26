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
engine = create_engine(
    url=os.path.join(f"sqlite+pysqlite:///{os.getcwd()}", "tests", "db.sqlite3"),
    echo=False,
)
TestingSession = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSession()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# creating fixures
random_id = str(uuid4())


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app=app)


@pytest.fixture(scope="session")
def base_route() -> str:
    return "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def fake_new_users() -> list[dict]:
    return [
        {"username": f"user_{random_id}_{i}", "password": random_id} for i in range(10)
    ]
