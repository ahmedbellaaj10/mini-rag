from typing import Optional
from pydantic import BaseModel, Field


class ProcessFileRequest(BaseModel):
    file_id: str = Field(..., description="The ID of the file.")
    chunk_size: Optional[int] = Field(
        100, description="The size of the chunk to read from the file."
    )
    overlap_size: Optional[int] = Field(
        20, description="The size of the overlap between chunks."
    )
    do_reset: Optional[bool] = Field(
        False, description="Whether to reset the file read position."
    )
