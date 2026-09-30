from fastapi import UploadFile

from .BaseController import BaseController


class DataController(BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.scale_size: int = 1024**2

    def validate_uploaded_file(self, file: UploadFile) -> tuple[bool, str]:

        if file is None or file.size is None:
            return False, "File is invalid"

        if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
            return False, "File type not supported"

        if file.size > self.settings.FILE_MAX_SIZE_MB * self.scale_size:
            return False, "File size exceeds the maximum allowed size"

        return True, "File is valid"
