import os
from pathlib import Path

from .BaseController import BaseController


class ProjectController(BaseController):
    def __init__(self) -> None:
        super().__init__()

    def get_project_path(self, project_id: str) -> Path:
        project_dir_path: Path = self.files_dir / project_id

        if not project_dir_path.exists():
            os.makedirs(project_dir_path, exist_ok=True)
        return project_dir_path
