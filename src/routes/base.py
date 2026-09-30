from fastapi import APIRouter, Depends

from config.config import Settings, get_settings

base_router: APIRouter = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@base_router.get("/")
async def read_root(app_settings: Settings = Depends(get_settings)) -> dict[str, str]:
    app_name: str = app_settings.APP_NAME
    app_version: str = app_settings.APP_VERSION
    return {"message": f"Welcome to {app_name} v{app_version}!"}
