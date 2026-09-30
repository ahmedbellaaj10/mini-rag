from fastapi import UploadFile

from .BaseController import BaseController
from models import ResponseSignal


class DataController(BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.scale_size: int = 1024**2

    def validate_uploaded_file(self, file: UploadFile) -> tuple[bool, str]:

        if file is None or file.size is None:
            return False, ResponseSignal.FILE_INVALID.value

        if file.filename is None or file.filename.strip() == "":
            return False, ResponseSignal.FILE_NAME_INVALID.value

        if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.settings.FILE_MAX_SIZE_MB * self.scale_size:
            return False, ResponseSignal.FILE_SIZE_EXCEEDS_LIMIT.value

        return True, ResponseSignal.FILE_VALID.value
