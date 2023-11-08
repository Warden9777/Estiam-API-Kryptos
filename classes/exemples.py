from pydantic import BaseModel
from typing import List
from classes.schema_dto import CryptoCurrency as CCModel

CryptoCurrency = [
    CCModel(id= "btc", name= "Bitcoin", amount= 1.5),
    CCModel(id= "eth", name= "Ethereum", amount= 10.2),
    CCModel(id= "ltc", name= "Litecoin", amount= 50.0),
]