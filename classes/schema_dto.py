from pydantic import BaseModel
from typing import List
from exemples import CryptoCurrency

class User(BaseModel):
    email: str
    password: str

class Wallet(BaseModel):
    user_id: str
    crypto_currencies: List[CryptoCurrency]

class CryptoCurrency(BaseModel):
    id: str
    name: str
    amount: float

class WalletBalance(BaseModel):
    user_id: str
    total_balance: float
    crypto_currencies: List[CryptoCurrency]
