import re

from pathlib import Path
from fastapi import UploadFile

from .BaseController import BaseController
from .ProjectController import ProjectController
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

    def generate_unique_filename(self, original_filename: str, project_id: str) -> Path:
        project_dir_path = ProjectController().get_project_path(project_id)
        random_key: str = super().generate_random_string()
        cleaned_filename: str = self.get_clean_filename(original_filename)

        new_filename: Path = project_dir_path / f"{random_key}_{cleaned_filename}"

        while new_filename.exists():
            random_key = super().generate_random_string()
            new_filename = project_dir_path / f"{random_key}_{cleaned_filename}"

        return new_filename

    def get_clean_filename(self, origin_filename: str) -> str:

        # remove any special caracters from the filename except the underscore and the dot
        cleaned_filename: str = re.sub(r"[^a-zA-Z0-9_.]", "", origin_filename.strip())
        cleaned_filename = cleaned_filename.replace(" ", "_")
        return cleaned_filename
