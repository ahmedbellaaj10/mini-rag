from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient

from config.config import get_settings
from routes import base, data
from stores.llm import LLMProviderFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    settings = get_settings()
    app.state.mongo_con = AsyncMongoClient(settings.MONGODB_URL)
    app.state.db = app.state.mongo_con[settings.MONGODB_DB_NAME]

    llm_provider_factory = LLMProviderFactory(config=settings.model_dump())

    app.state.llm_provider = llm_provider_factory.create_provider(
        settings.GENERATION_BACKEND
    )
    app.state.llm_provider.set_llm(settings.LLM_ID)

    app.state.embedding_provider = llm_provider_factory.create_provider(
        settings.EMBEDDING_BACKEND
    )
    app.state.embedding_provider.set_embedding_model(
        settings.EMBEDDING_MODEL_ID, settings.EMBEDDING_MODEL_SIZE
    )

    yield  # app runs while suspended here

    # --- shutdown ---
    await app.state.mongo_con.close()


app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
