from fastapi import FastAPI
from documentation.description import api_description
from documentation.tags import tags_metadata


app = FastAPI(
    title="Kryptos",  
    description=api_description,  
    openapi_tags=tags_metadata,
    docs_url='/' 
)