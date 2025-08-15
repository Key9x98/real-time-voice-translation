# Quản lý cấu hình dự án theo chuẩn OOP

from src.utils.config_loader import ConfigLoader
from src.utils.env_utils import EnvUtils

class ProjectConfig:
    _instance = None

    def __new__(cls, config_path: str = "config.yaml", env_path: str = ".env"):
        if cls._instance is None:
            cls._instance = super(ProjectConfig, cls).__new__(cls)
            cls._instance._init_config(config_path, env_path)
        return cls._instance

    def _init_config(self, config_path, env_path):
        self._loader = ConfigLoader(config_path)
        self._env = EnvUtils(env_path)
        self._config = self._loader.load()

    def get(self, key, default=None):
        # Ưu tiên lấy từ biến môi trường nếu là API key
        if key.endswith("API_KEY"):
            value = self._env.get(key)
            if value:
                return value
        return self._config.get(key, default)

    def reload(self):
        self._config = self._loader.load()

# Ví dụ sử dụng:
# config = ProjectConfig()
# api_key = config.get("ASSEMBLY_API_KEY")
# model_name = config.get("TRANSLATION_MODEL")
