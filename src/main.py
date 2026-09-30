from fastapi import FastAPI

from routes import base

app: FastAPI = FastAPI()

app.include_router(base.base_router)
