from fastapi.testclient import TestClient
from main import app
from main import HelloResp
from json import dumps
import pytest

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}


@pytest.mark.parametrize("name", ['Zenek', 'Marek', 'Alojzy Niezdąży'])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert dumps(response.json()) == dumps(HelloResp(message=f"Hello {name}").__dict__)


def test_counter():
    response = client.get("/counter")
    assert response.status_code == 200
    assert "1" == response.text
    response = client.get("/counter")
    assert response.status_code == 200
    assert "2" == response.text


def test_receive_something():
    response = client.post("/giveme", json={'first_key': 'some_value'})
    assert response.json() == {"received": {'first_key': 'some_value'},
                             "constant_data": "python jest super"}