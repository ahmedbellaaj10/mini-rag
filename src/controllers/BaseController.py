import random
import string

from pathlib import Path

from config.config import Settings, get_settings


class BaseController:
    def __init__(self) -> None:
        self.settings: Settings = get_settings()
        self.base_dir: Path = Path(__file__).resolve().parents[2]
        self.files_dir: Path = self.base_dir / "assets" / "files"

    def generate_random_string(self, length: int = 12) -> str:
        """
        Generate a unique string.
        This method can be overridden in subclasses to implement custom logic for generating unique strings.

        Args:
            length (int): The length of the generated string. Default is 12.
        Returns:
            str: A unique string.
        """
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))
