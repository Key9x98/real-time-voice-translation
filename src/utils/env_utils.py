# Tiện ích quản lý biến môi trường
import os
from dotenv import load_dotenv

class EnvUtils:
	def __init__(self, env_path: str = ".env"):
		self.env_path = env_path
		load_dotenv(self.env_path)

	def get(self, key: str, default=None):
		return os.getenv(key, default)
