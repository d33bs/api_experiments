import os
import sys
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient

from app.fastapi_main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_items():
    response = client.get("/items/1", params={"q": "first item description"})
    assert response.status_code == 200
    assert response.json() == {"item_id": 1,"q": "first item description"}