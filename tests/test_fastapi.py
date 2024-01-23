from fastapi.testclient import TestClient
from main import api

client = TestClient(api)

def test_docs():
  response = client.get("/")
  assert response.status_code == 200

def test_redoc():
  response = client.get('/redoc')
  assert response.status_code == 200