import aiofiles
import logging
import os

from bson import ObjectId
from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse

from config.config import Settings, get_settings
from controllers import DataController, ProcessFileController
from models import ResponseSignal
from schemes import ProcessFileRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from models.db_schemes import DataChunk, Asset
from models.enums.AssetTypeEnums import AssetTypeEnum

logger = logging.getLogger("uvicorn.error")

data_router: APIRouter = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1, data"],
)


@data_router.post("/upload/{project_id}")
async def upload_data(
    request: Request,
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings),
) -> JSONResponse:

    project_model: ProjectModel = await ProjectModel.create_instance(
        db_client=request.app.state.db
    )

    project = await project_model.get_project_or_create_one(project_id)

    data_controller = DataController()
    # validate file properties
    is_valid_file, result_message = data_controller.validate_uploaded_file(file)

    if not is_valid_file:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "is_valid_file": is_valid_file,
                "project_id": project.id,
                "message": result_message,
            },
        )

    if file.filename is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "is_valid_file": False,
                "project_id": project.id,
                "message": "File name is missing",
            },
        )

    file_path, file_id = data_controller.generate_unique_filepath(
        file.filename, project_id
    )

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(
                app_settings.FILE_DEFAULT_CHUNK_SIZE_MB * DataController().scale_size
            ):
                await f.write(chunk)

        # store asset (files for now) in the db
        asset_model: AssetModel = await AssetModel.create_instance(
            db_client=request.app.state.db
        )

        assert isinstance(project.id, ObjectId), "Project ID must be an ObjectId"

        asset = Asset(
            asset_project_id=project.id,
            asset_type=AssetTypeEnum.FILE.value,
            asset_name=file_id,
            asset_size=os.path.getsize(file_path),
        )
        await asset_model.create_asset(asset)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "is_valid_file": is_valid_file,
                "message": result_message,
                "file_id": file_id,
            },
        )
    except Exception as e:
        logger.error(f"Error occurred while uploading the file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "is_valid_file": False,
                "project_id": project.id,
                "message": ResponseSignal.FILE_UPLOAD_FAILED.value,
            },
        )


@data_router.post("/process/{project_id}")
async def process_file(
    project_id: str,
    file_processing: ProcessFileRequest,
    request: Request,
) -> JSONResponse:
    file_id = file_processing.file_id
    process_file_controller = ProcessFileController(project_id)
    file_content = process_file_controller.get_file_content(file_id)
    file_chunks = process_file_controller.process_file_content(
        file_content,
        chunk_size=file_processing.chunk_size,
        overlap_size=file_processing.overlap_size,
    )

    project_model: ProjectModel = await ProjectModel.create_instance(
        db_client=request.app.state.db
    )

    project = await project_model.get_project_or_create_one(project_id)

    chunk_model: ChunkModel = await ChunkModel.create_instance(
        db_client=request.app.state.db
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "project_id": project_id,
                "file_id": file_id,
                "message": ResponseSignal.FILE_PROCESSING_FAILED.value,
            },
        )

    if file_processing.do_reset:
        await chunk_model.delete_chunks_by_project_id(ObjectId(project.id))

    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=index + 1,
            chunk_project_id=ObjectId(project.id),
        )
        for index, chunk in enumerate(file_chunks)
    ]

    num_inserted_chunks = await chunk_model.insert_many_chunks(file_chunks_records)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "project_id": str(project.id),
            "file_id": file_id,
            "message": ResponseSignal.FILE_PROCESSING_SUCCESS.value,
            "num_inserted_chunks": num_inserted_chunks,
        },
    )
