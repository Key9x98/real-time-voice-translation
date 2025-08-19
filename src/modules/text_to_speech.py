
# Text-to-Speech module
# OOP design, easily extensible for multiple TTS providers

import sounddevice as sd
import numpy as np
from transformers import pipeline

class TextToSpeech:
	def __init__(self, model_name: str = "suno/bark"):
		self.model_name = model_name
		self.pipe = pipeline("text-to-speech", model=self.model_name)

	def synthesize(self, text: str):
		output = self.pipe(text)
		audio = output["audio"]
		print("=== KIỂM TRA ĐẦU RA TTS ===")
		print("Text đầu vào:", text)
		print("AUDIO TYPE:", type(audio))
		print("AUDIO SHAPE:", getattr(audio, 'shape', None))
		if isinstance(audio, np.ndarray):
			print("Min:", np.min(audio), "Max:", np.max(audio))
			print("Sampling rate:", output.get("sampling_rate", "Không có"))
			if len(audio.shape) == 2:
				audio = np.squeeze(audio)
			sd.play(audio, output["sampling_rate"])
			sd.wait()
		else:
			print("Không phải dữ liệu âm thanh thực. Đầu ra:", audio)

# Example usage
if __name__ == "__main__":
	tts = TextToSpeech()
	tts.synthesize("To improve the model's accuracy, you should use it as a pretrained base. I can recommend the Emilia dataset for this purpose. After the pretraining process is complete, you should perform fine-tuning for single-speaker speech.")