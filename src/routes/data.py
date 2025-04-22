from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import Settings, get_settings
from controllers import DataController, ProjectController
from models import ResponseSignal
import aiofiles
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    # validate file properties
    is_valid, result_signal = DataController().validate_uploaded_file(file)

    if not is_valid:
        return JSONResponse(
            content={"signal": result_signal},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    
    # project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path = DataController().generate_unique_filename(
        original_filename=file.filename,
        project_id=project_id
    )
    
    try :
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        return JSONResponse(
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return JSONResponse(
        content={"signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value},  
        status_code=status.HTTP_200_OK,     
    )
