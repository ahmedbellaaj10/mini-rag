from pathlib import Path

from config.config import Settings, get_settings


class BaseController:
    def __init__(self) -> None:
        self.settings: Settings = get_settings()
        self.base_dir: Path = Path(__file__).resolve().parents[2]
        self.files_dir: Path = self.base_dir / "assets" / "files"
