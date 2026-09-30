import aiofiles

from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from pathlib import Path

from config.config import Settings, get_settings
from controllers import DataController, ProjectController

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

    if file.filename is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "is_valid_file": False,
                "project_id": project_id,
                "message": "File name is missing",
            },
        )

    project_dir_path: Path = ProjectController().get_project_path(project_id)
    file_path: Path = project_dir_path / file.filename

    async with aiofiles.open(file_path, "wb") as f:
        while chunk := await file.read(
            app_settings.FILE_DEFAULT_CHUNK_SIZE_MB * DataController().scale_size
        ):
            await f.write(chunk)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "is_valid_file": is_valid_file,
            "project_id": project_id,
            "message": result_message,
        },
    )
