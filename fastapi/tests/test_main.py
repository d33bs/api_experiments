import os
import sys

sys.path.append(os.getcwd())
sys.path.append("{}/app".format(os.getcwd()))

from app.fastapi_main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_items():
    response = client.get("/items/1", params={"q": "first item description"})
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "q": "first item description"}


def test_get_sklearn_wine():
    response = client.get("/sklearn_wine")
    assert response.status_code == 200
    assert len(response.json()) == 178


def test_get_sqlite_wine():
    # response = client.get("/sklearn_wine")
    response = client.get("/sqlite_wine")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
