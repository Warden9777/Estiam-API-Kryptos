from pydantic import BaseModel
from typing import List

class User(BaseModel):
    email: str
    password: str

class CryptoCurrency(BaseModel):
    id: str
    name: str
    amount: float

class Wallet(BaseModel):
    user_id: str
    crypto_currencies: List[CryptoCurrency]

class WalletBalance(BaseModel):
    user_id: str
    total_balance: float
    crypto_currencies: List[CryptoCurrency]
