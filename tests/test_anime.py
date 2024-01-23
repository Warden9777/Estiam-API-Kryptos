from fastapi.testclient import TestClient
from main import api
import pytest
from classes.models import CryptoCurrency, Wallet, WalletBalance

client = TestClient(api)

def wallet_uids():
 response = client.get("/wallets")
 uid_list = [wallet['uid'] for wallet in response.json()]
 if len(uid_list) > 5 :
  uid_list = uid_list[0:5]
 return uid_list


def test_get_all_wallets():
 response = client.get("/wallets")
 assert response.status_code == 200
 assert type(response.json()) is list

@pytest.mark.parametrize("route,method,body", [
 ("/wallets","POST", Wallet().model_dump()),
 ("/wallets/walletUID","PUT", Wallet().model_dump()),
 ("/wallets/walletUID","DELETE", None)
])
def test_unauthorized(route, method, body):
 if (method == "GET"):
  response = client.get(route)
 elif (method == "POST"):
  response = client.post(route, json=body)
 elif (method == "PUT"):
  response = client.put(route, json=body)
 elif (method == "PATCH"):
  response = client.patch(route, json=body)
 elif (method == "DELETE"):
  response = client.delete(route)
  
 assert response.status_code == 401

@pytest.mark.parametrize("wallet",[
 Wallet(
  user_id="user1",
  crypto_currencies=[CryptoCurrency(id="crypto1", name="Bitcoin", amount=0.1), CryptoCurrency(id="crypto2", name="Ethereum", amount=0.2)])
])
def test_post_valid_wallet(wallet, auth_user):
 response = client.post("/wallets", json= wallet.model_dump(), headers={
  "Authorization": f"Bearer {auth_user['access_token']}"
 })
 assert response.status_code == 201
 assert type(response.json()) == dict

@pytest.mark.parametrize("something",[
 {"example": "this is obviously not working"},
 {"user_id":"not an id", "crypto_currencies":[
  {"id":"crypto1", "name":"Bitcoin"},
  {"id":"crypto2", "name":"Ethereum"}
 ]},
 {"user_id":"user1", "crypto_currencies":[
  {"id":"crypto1", "name":"Bitcoin", "amount":"invalid amount"}
 ]}
])
def test_post_invalid_wallet(something, auth_user):
 response = client.post("/wallets", json= something, headers={
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


def test_update_wallet(auth_user, create_wallet):
 updated_wallet = Wallet(
  user_id="user1",
  crypto_currencies=[CryptoCurrency(id="crypto1", name="Bitcoin", amount=0.9), CryptoCurrency(id="crypto2", name="Ethereum", amount=0.4)])
 response = client.put(f"/wallets/{create_wallet['uid']}", headers={
  "Authorization": f"Bearer {auth_user['access_token']}"
 }, json= updated_wallet.model_dump())
 response.status_code ==
