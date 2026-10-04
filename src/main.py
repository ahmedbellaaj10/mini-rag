from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient

from config.config import get_settings
from routes import base, data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    settings = get_settings()
    app.state.mongo_con = AsyncMongoClient(settings.MONGODB_URL)
    app.state.db = app.state.mongo_con[settings.MONGODB_DB_NAME]

    yield  # app runs while suspended here

    # --- shutdown ---
    await app.state.mongo_con.close()


app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
