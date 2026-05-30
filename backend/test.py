import pytest

def func(x):
    return x + 1


def test_answer():
    assert func(4) == 5

def add(x, y):
    return x + y


@pytest.mark.parametrize("a,b,expected", [(1,2,3),(0,0,0),(2,4,6)])
def test_add_many(a, b, expected):
    assert add(a, b) == expected


#FastAPI test client example
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Hello World"}

def test_root_message():
    response = client.get("/")
    assert response.json()["message"] == "Hello World"

# Code Execution command: pytest .\backend\test.py