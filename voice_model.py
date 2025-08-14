import sounddevice as sd
print("Thiết bị phát âm thanh mặc định:")
print(sd.query_devices(kind='output'))



from transformers import pipeline
import sounddevice as sd
import numpy as np
import soundfile as sf
import io

def play_voice(text: str):
    pipe = pipeline("text-to-speech", model="suno/bark")
    output = pipe(text)
    audio = output["audio"]
    print("=== KIỂM TRA ĐẦU RA TTS ===")
    print("Text đầu vào:", text)
    print("AUDIO TYPE:", type(audio))
    print("AUDIO SHAPE:", getattr(audio, 'shape', None))
    if isinstance(audio, np.ndarray):
        print("Min:", np.min(audio), "Max:", np.max(audio))
        print("Sampling rate:", output.get("sampling_rate", "Không có"))
        # Nếu dữ liệu là (1, N) hoặc (N, 1), chuyển về 1 chiều
        if len(audio.shape) == 2:
            audio = np.squeeze(audio)
        sd.play(audio, output["sampling_rate"])
        sd.wait()
    else:
        print("Không phải dữ liệu âm thanh thực. Đầu ra:", audio)


if __name__ == "__main__":
    play_voice("To improve the model's accuracy, you should use it as a pretrained base. I can recommend the Emilia dataset for this purpose. After the pretraining process is complete, you should perform fine-tuning for single-speaker speech.")

