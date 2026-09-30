from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse

from config.config import Settings, get_settings
from controllers import DataController

data_router: APIRouter = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1, data"],
)


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)
):
    # validate file properties
    is_valid_file, result_message = DataController().validate_uploaded_file(file)

    if not is_valid_file:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "is_valid_file": is_valid_file,
                "project_id": project_id,
                "message": result_message,
            },
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "is_valid_file": is_valid_file,
            "project_id": project_id,
            "message": result_message,
        },
    )
