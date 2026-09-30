from config.config import Settings, get_settings


class BaseController:
    def __init__(self) -> None:
        self.settings: Settings = get_settings()
