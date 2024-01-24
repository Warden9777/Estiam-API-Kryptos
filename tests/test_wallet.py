from fastapi.testclient import TestClient
import pytest
from firebase_admin import credentials
from firebase_admin import auth
from database import firebase
from main import api
from classes.schema_dto import CryptoCurrency, Wallet

client = TestClient(api)

def wallet_uids():
    response = client.get("/wallets")
    # Vérifiez que la réponse est un dictionnaire (ou une liste, si nécessaire)
    if isinstance(response.json(), dict):
        uid_list = list(response.json().keys())[:5]
    else:
        uid_list = []
    return uid_list

def test_get_all_wallets():
    response = client.get("/wallets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.parametrize("route, method, body", [
    ("/wallets", "POST", Wallet(
        user_id="user1",
        crypto_currencies=[
            CryptoCurrency(id="crypto1", name="Bitcoin", amount=0.1),
            CryptoCurrency(id="crypto2", name="Ethereum", amount=0.2)
        ]
    ).model_dump()),
    ("/wallets/walletUID", "PUT", Wallet(
        user_id="user1",
        crypto_currencies=[
            CryptoCurrency(id="crypto1", name="Bitcoin", amount=0.1),
            CryptoCurrency(id="crypto2", name="Ethereum", amount=0.2)
        ]
    ).model_dump()),
    ("/wallets/walletUID", "DELETE", None)
])
def test_unauthorized(route, method, body, auth_user):
    headers = {"Authorization": f"Bearer {auth_user['access_token']}"}
    if method == "GET":
        response = client.get(route, headers=headers)
    elif method == "POST":
        response = client.post(route, json=body, headers=headers)
    elif method == "PUT":
        response = client.put(route, json=body, headers=headers)
    elif method == "DELETE":
        response = client.delete(route, headers=headers)
    assert response.status_code == 401

@pytest.mark.parametrize("something", [
    {"example": "this is obviously not working"},
    {"user_id": "not an id", "crypto_currencies": [
        {"id": "crypto1", "name": "Bitcoin"},
        {"id": "crypto2", "name": "Ethereum"}
    ]},
    {"user_id": "user1", "crypto_currencies": [
        {"id": "crypto1", "name": "Bitcoin", "amount": "invalid amount"}
    ]}
])
def test_post_invalid_wallet(something, auth_user):
    response = client.post("/wallets", json=something, headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert response.status_code == 422

@pytest.mark.parametrize("id", wallet_uids())
def test_get_wallet_by_id(id):
    response = client.get(f'/wallets/{id}')
    assert response.status_code == 200

@pytest.mark.parametrize("id", ["not an id", "still not", "i think it's enough testing now"])
def test_get_wallet_not_found(id):
    response = client.get(f'/wallets/{id}')
    assert response.status_code == 404

@pytest.mark.parametrize("id", wallet_uids())
def test_update_wallet(id, auth_user):
    updated_wallet = Wallet(
        user_id="user1",
        crypto_currencies=[
            CryptoCurrency(id="crypto1", name="Bitcoin", amount=0.9),
            CryptoCurrency(id="crypto2", name="Ethereum", amount=0.4)
        ]
    )
    response = client.put(f"/wallets/{id}", json=updated_wallet.model_dump(), headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert response.status_code == 201

@pytest.mark.parametrize("id", wallet_uids())
def test_delete_wallet(id, auth_user):
    response = client.delete(f'/wallets/{id}', headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert response.status_code == 204