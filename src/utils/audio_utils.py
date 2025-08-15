# Tiện ích xử lý âm thanh
import numpy as np
import soundfile as sf

class AudioUtils:
	@staticmethod
	def normalize(audio: np.ndarray) -> np.ndarray:
		return audio / np.max(np.abs(audio))

	@staticmethod
	def save_wav(audio: np.ndarray, sample_rate: int, filename: str):
		sf.write(filename, audio, sample_rate)

	@staticmethod
	def load_wav(filename: str):
		audio, sr = sf.read(filename)
		return audio, sr
