from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
import uuid

# Modèle Pydantic pour la gestion des portefeuilles de cryptomonnaies
class CryptoWallet(BaseModel):
    id: str
    user_id: str
    crypto_currencies: List[CryptoCurrency]

class CryptoCurrency(BaseModel):
    id: str
    name: str
    amount: float

# Liste de données pour les portefeuilles de cryptomonnaies (simulé)
crypto_wallets = []

# Créez un routeur pour la gestion des portefeuilles de cryptomonnaies
router = APIRouter(
    tags=["CryptoWallets"]
)

# Endpoint pour créer un portefeuille de cryptomonnaies
@router.post('/crypto-wallets', status_code=201)
async def create_crypto_wallet(crypto_wallet: CryptoWallet):
    # Générer un nouvel ID unique pour le portefeuille
    crypto_wallet.id = str(uuid.uuid4())
    crypto_wallets.append(crypto_wallet)
    return crypto_wallet

# Endpoint pour obtenir un portefeuille par ID
@router.get('/crypto-wallets/{wallet_id}')
async def get_crypto_wallet(wallet_id: str):
    for wallet in crypto_wallets:
        if wallet.id == wallet_id:
            return wallet
    raise HTTPException(status_code=404, detail="Crypto wallet not found")

# Endpoint pour obtenir la liste de tous les portefeuilles de cryptomonnaies
@router.get('/crypto-wallets', response_model=List[CryptoWallet])
async def get_all_crypto_wallets():
    return crypto_wallets

# Endpoint pour mettre à jour un portefeuille de cryptomonnaies
@router.put('/crypto-wallets/{wallet_id}', response_model=CryptoWallet)
async def update_crypto_wallet(wallet_id: str, updated_wallet: CryptoWallet):
    for wallet in crypto_wallets:
        if wallet.id == wallet_id:
            wallet.user_id = updated_wallet.user_id
            wallet.crypto_currencies = updated_wallet.crypto_currencies
            return wallet
    raise HTTPException(status_code=404, detail="Crypto wallet not found")

# Endpoint pour supprimer un portefeuille de cryptomonnaies par ID
@router.delete('/crypto-wallets/{wallet_id}', status_code=204)
async def delete_crypto_wallet(wallet_id: str):
    for wallet in crypto_wallets:
        if wallet.id == wallet_id:
            crypto_wallets.remove(wallet)
            return
    raise HTTPException(status_code=404, detail="Crypto wallet not found")

# Vous pouvez ajouter d'autres fonctionnalités, telles que l'ajout, le retrait ou l'échange de cryptomonnaies dans le portefeuille.
