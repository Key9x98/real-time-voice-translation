# Speech-to-Text module
# Implement AssemblyAI or other STT logic here

import os
from faster_whisper import WhisperModel, BatchedInferencePipeline
import re

class SpeechToText:
    def __init__(self,input_audio: str = "audio.mp3", model_name: str = "base", device: str = "cpu", compute_type: str = "int8"):
        self.input_audio = input_audio
        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)
        self.pipeline = BatchedInferencePipeline(self.model)

    def clean_text(self, text: str) -> str:
        """
        Làm sạch văn bản, loại bỏ các ký tự không cần thiết. 
        """
        return re.sub(r'\s+', ' ', text).strip()

    def preprocess_transcript(self, segments: list) -> list:
        """
        Tiền xử lý transcript, trả về dict với data:
        - start: thời gian đoạn văn bắt đầu.
        - end: thời gian đoạn văn kết thúc.
        - text: nội dung văn bản đã chuyển đổi.
        """
        processed_segments = []
        for segment in segments:
            processed_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": self.clean_text(segment.text)
            })
        return processed_segments

    def transcript_audio(self, input_audio: str = "audio.mp3", model_name: str = "base", device: str = "cpu", compute_type: str = "int8", beam_size: int = 5, vad_filter: bool = True) -> tuple:
        """
        Chuyển đổi âm thanh thành văn bản.
        """
        if not os.path.exists(input_audio):
            raise FileNotFoundError(f"Không tìm thấy file âm thanh: {input_audio}")
        
        # Khởi tạo model
        model = WhisperModel(model_name, device=device, compute_type=compute_type)
        
        # Cấu hình cho tham số:
        transcript_kwargs = {"beam_size": beam_size}
        
        if vad_filter:
            transcript_kwargs["vad_filter"] = vad_filter
            
        # Chạy transcription:
        batch_model = BatchedInferencePipeline(model)
        segments, info = batch_model.transcribe(input_audio, **transcript_kwargs, batch_size=16)
        # Tiền xử lý kết quả:
        segments = list(segments)
        processed_segments = self.preprocess_transcript(segments)
        return processed_segments, info

    def save_transcript(self, segments: list, output_file: str) -> None:
        """
        Lưu transcript vào file.
        """
        with open(output_file, "w", encoding="utf-8") as f:
            for segment in segments:
                # f.write(f"{segment['start']} --> {segment['end']}\n{segment['text']}\n\n")
                f.write(f"{segment['text']}\n")