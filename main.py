from fastapi import FastAPI
import routers.routers_accounts
import routers.routers_auth
import routers.routers_stripe
import routers.routers_wallet
from documentation.description import api_description
from documentation.tags import tags_metadata

#api init (launch with uvicorn main:api --reload)
api = FastAPI( 
    title="Kryptos",
    description=api_description,
    openapi_tags=tags_metadata, 
    docs_url='/'
)

api.include_router(routers.routers_accounts.router)
api.include_router(routers.routers_auth.router)
api.include_router(routers.routers_stripe.router)
api.include_router(routers.routers_wallet.router)