# Tiện ích tải cấu hình dự án
import os
import yaml

class ConfigLoader:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = None

    def load(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Không tìm thấy file cấu hình: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        return self.config

    def get(self, key, default=None):
        if self.config is None:
            self.load()
        return self.config.get(key, default)
