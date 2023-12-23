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
