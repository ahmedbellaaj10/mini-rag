from fastapi import APIRouter
import os
from typing import Optional

base_router: APIRouter = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@base_router.get("/")
async def read_root() -> dict[str, str]:
    app_name: Optional[str] = os.getenv("APP_NAME")
    app_version: Optional[str] = os.getenv("APP_VERSION")
    return {"message": f"Welcome to {app_name} v{app_version}!"}
