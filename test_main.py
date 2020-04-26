from fastapi.testclient import TestClient
from main import HelloResp, MethodResp, app
from json import dumps
import pytest

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}


@pytest.mark.parametrize("name", ['Zenek', 'Marek', 'Alojzy Niezdąży']) #3 tests
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


def test_method():
    response = client.get("/method")
    assert response.status_code == 200
    assert dumps(response.json()) == dumps(MethodResp(method="GET").__dict__)
    response = client.post("/method")
    assert response.status_code == 200
    assert dumps(response.json()) == dumps(MethodResp(method="POST").__dict__)
    response = client.put("/method")
    assert response.status_code == 200
    assert dumps(response.json()) == dumps(MethodResp(method="PUT").__dict__)
    response = client.delete("/method")
    assert response.status_code == 200
    assert dumps(response.json()) == dumps(MethodResp(method="DELETE").__dict__)


def test_post_patient_with_id():
    response = client.post("/patient", json={'name': 'Name', 'surename': 'Surname'})
    assert response.status_code == 200
    assert response.json() == {"id": 0, "patient": {"name": "Name", "surename": "Surname"}}


def test_get_patient():
    patient_id = client.post("/patient", json={'name': 'Name', 'surename': 'Surname'}).json()["id"]
    response = client.get(f"/patient/{patient_id}")
    assert response.status_code == 200
    assert response.json() == {"name": "Name", "surename": "Surname"}