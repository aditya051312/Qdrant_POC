from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from v1.api import v1_router

app = FastAPI()

# app.mount("/static", StaticFiles(directory="text_vector"), name="static")

app.include_router(v1_router)
