import gradio as gr
import os
from src.modules.speech_to_text import SpeechToText


def process_audio_to_doc(input_audio: str) -> str:
    """
    Nhận 1 file audio -> Chuyển thành văn bản
    """
    s2t = SpeechToText()
    if not os.path.exists(input_audio):
        raise FileNotFoundError(f"Không tìm thấy file âm thanh: {input_audio}")

    # Chuyển đổi âm thanh thành văn bản
    transcript, info = s2t.transcript_audio(input_audio)
    temp_path = "temp_transcript.txt"
    print(f"Transcript: {transcript}")

    s2t.save_transcript(transcript, temp_path)

    return temp_path

# Xây dựng 1 giao diện gradio
iface = gr.Interface(
    fn=process_audio_to_doc,
    inputs=gr.Audio(type="filepath", label="Tải lên file audio"),
    outputs= "textbox",
    title="Chuyển đổi âm thanh thành văn bản",
    description="Tải audio và trả về văn bản đã chuyển đổi"
)

if __name__ == "__main__":
    iface.launch()