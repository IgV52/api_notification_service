from fastapi.testclient import TestClient
from main import create_app

app = create_app()

test_app = TestClient(app)

def test_get_main():
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello world"}
