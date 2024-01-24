from fastapi.testclient import TestClient
from main import api
from firebase_admin import credentials
from firebase_admin import auth
from database import firebase
import pytest
from classes.schema_dto import User

client = TestClient(api)

def user_emails():
    response = client.get("/user-accounts")
    email_list = [user['email'] for user in response.json()]
    if len(email_list) > 5:
        email_list = email_list[0:5]
    return email_list

def test_get_all_user_accounts():
    response = client.get("/user-accounts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.parametrize("route, method, body", [
    ("/user-accounts", "POST", User(email="test@example.com", password="secure_password").model_dump()),
    ("/user-accounts/user_email", "PUT", User(email="test@example.com", password="secure_password").model_dump()),
    ("/user-accounts/user_email", "DELETE", None)
])
def test_unauthorized(route, method, body):
    headers = {"Authorization": "Bearer invalid_token"}

    if method == "GET":
        response = client.get(route, headers=headers)
    elif method == "POST":
        response = client.post(route, json=body, headers=headers)
    elif method == "PUT":
        response = client.put(route, json=body, headers=headers)
    elif method == "DELETE":
        response = client.delete(route, headers=headers)

    assert response.status_code == 401

@pytest.mark.parametrize("user", [
    User(email="test@example.com", password="secure_password")
])
def test_post_valid_user(user, auth_user):
    response = client.post("/user-accounts", json=user.model_dump(), headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert response.status_code == 201
    assert isinstance(response.json(), dict)

@pytest.mark.parametrize("something", [
    {"example": "this is obviously not working"},
    {"email": "missing_password@example.com"},
    {"password": "missing_email"},
    {"email": "user@example.com", "password": "short"}
])
def test_post_invalid_user(something, auth_user):
    response = client.post("/user-accounts", json=something, headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert response.status_code == 422

@pytest.mark.parametrize("email", user_emails())
def test_get_user_by_email(email):
    response = client.get(f'/user-accounts/{email}')
    assert response.status_code == 200

def test_update_user(auth_user, create_user):
    updated_user = User(email="updated_user@example.com", password="updated_password")
    response = client.put(f"/user-accounts/{create_user['email']}", json=updated_user.model_dump(), headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert response.status_code == 200

def test_delete_user(auth_user, create_user):
    response = client.delete(f"/user-accounts/{create_user['email']}", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert response.status_code == 204

@pytest.mark.parametrize("email", ["not_an_email@example.com", "still_not@example.com", "enough_testing_now@example.com"])
def test_get_update_delete_user_not_found(email, auth_user):
    user = User(email="test@example.com", password="secure_password").model_dump()

    response = client.get(f'/user-accounts/{email}')
    assert response.status_code == 404

    response = client.put(f"/user-accounts/{email}", json=user, headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert response.status_code == 404

    response = client.delete(f"/user-accounts/{email}", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert response.status_code == 404