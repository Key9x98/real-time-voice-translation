# Custom Instructions cho Dự án Dịch Giọng Nói Thời Gian Thực

## Bối cảnh và Mục tiêu Dự án

- **Dự án**: Real Time Voice Translation (Dịch giọng nói thời gian thực).
- **Mục tiêu**: Xây dựng một hệ thống có khả năng nhận dạng giọng nói đầu vào, dịch sang ngôn ngữ đích và phát lại bằng giọng nói đã được tổng hợp, tất cả diễn ra với độ trễ thấp nhất có thể.
- **Vai trò của tôi**: AI Engineer, chịu trách nhiệm thiết kế, triển khai và tối ưu hóa các mô hình AI/ML, cũng như cấu trúc tổng thể của pipeline xử lý dữ liệu.

---

## Yêu cầu về Ngôn ngữ và Phong cách Code

- **Ngôn ngữ chính**: Python.
- **Chuẩn lập trình**: Luôn tuân thủ nghiêm ngặt **Lập trình Hướng đối tượng (OOP)**. Mọi đoạn code được tạo ra phải được đóng gói trong các class và method hợp lý.
- **Ngôn ngữ phản hồi**: Luôn luôn giao tiếp và giải thích code bằng **tiếng Việt**.

---

## Cấu trúc và Tổ chức Dự án

Khi đề xuất cấu trúc file hoặc project, hãy tuân thủ theo mô hình sau để đảm bảo tính module và dễ bảo trì:

- **`/src`**: Chứa toàn bộ mã nguồn của ứng dụng.
    - **`/src/core`**: Các class, module cốt lõi của hệ thống.
        - `pipeline.py`: Class `TranslationPipeline` để điều phối toàn bộ luồng xử lý.
        - `config.py`: Quản lý các cấu hình của dự án.
    - **`/src/modules`**: Chứa các module chức năng riêng biệt.
        - **`/speech_recognition`**:
            - `recognizer.py`: Class `SpeechRecognizer` sử dụng AssemblyAI để chuyển giọng nói thành văn bản (Speech-to-Text).
        - **`/translation`**:
            - `translator.py`: Class `Translator` sử dụng các mô hình Transformer từ Hugging Face để dịch văn bản.
        - **`/speech_synthesis`**:
            - `synthesizer.py`: Class `SpeechSynthesizer` để chuyển văn bản đã dịch thành giọng nói (Text-to-Speech).
    - **`/src/utils`**: Các hàm, class tiện ích sử dụng chung.
    - **`/src/api`**: Nếu có, chứa các file liên quan đến API (ví dụ: FastAPI, Flask).
- **`/main.py`**: Điểm khởi chạy của ứng dụng.
- **`/notebooks`**: Chứa các file Jupyter Notebook để thử nghiệm và phân tích.
- **`/tests`**: Chứa code unit test cho các module.

---

## Hướng dẫn chi tiết về Công nghệ và Thư viện

### 1. **Python - Lập trình Hướng đối tượng (OOP)**

- **Encapsulation (Đóng gói)**: Dữ liệu và các phương thức xử lý dữ liệu đó phải được gói gọn trong một class. Sử dụng các thuộc tính `private` (ví dụ: `_variable`) khi cần thiết.
- **Inheritance (Kế thừa)**: Khi có các module với chức năng tương tự (ví dụ: nhiều nhà cung cấp dịch vụ Speech-to-Text khác nhau), hãy đề xuất một `BaseRecognizer` class và cho các class cụ thể kế thừa từ nó.
- **Polymorphism (Đa hình)**: Tận dụng tính đa hình để dễ dàng thay thế các component trong pipeline.
- **Abstraction (Trừu tượng)**: Các class nên che giấu sự phức tạp bên trong và chỉ cung cấp một giao diện (public methods) đơn giản để tương tác.
- **Design Patterns**: Ưu tiên sử dụng các design pattern phù hợp như Singleton cho các class quản lý tài nguyên (ví dụ: model), hoặc Factory để tạo ra các đối tượng xử lý khác nhau.

### 2. **AssemblyAI (Speech-to-Text)**

- Sử dụng **Real-Time Transcription** API của AssemblyAI.
- Đóng gói logic tương tác với AssemblyAI vào một class `AssemblyAIReconizer`.
- Class này phải có các method để:
    - `connect()`: Thiết lập kết nối WebSocket.
    - `stream(audio_chunk)`: Gửi các đoạn audio.
    - `get_transcript()`: Nhận và xử lý kết quả văn bản trả về.
    - `close()`: Đóng kết nối.
- Luôn có cơ chế xử lý lỗi kết nối và tái kết nối.

### 3. **Transformer & Hugging Face (Dịch thuật)**

- Sử dụng thư viện `transformers` của Hugging Face.
- Ưu tiên các mô hình được tối ưu cho tốc độ và hiệu năng dịch thuật real-time (ví dụ: `Helsinki-NLP/opus-mt-*`, T5-small, hoặc các mô hình được chưng cất - distilled models).
- Đóng gói model và tokenizer vào một class `HuggingFaceTranslator`.
- Method `translate(text, target_lang)` phải nhận văn bản đầu vào và trả về văn bản đã dịch.
- Tối ưu hóa việc tải model: chỉ tải model một lần và tái sử dụng (có thể áp dụng Singleton pattern).

### 4. **Langchain (Điều phối và Mở rộng)**

- Khi cần xây dựng các chuỗi xử lý phức tạp hơn hoặc tích hợp với các mô hình ngôn ngữ lớn (LLM), hãy sử dụng Langchain.
- Đề xuất sử dụng các `Chain` của Langchain để kết nối các bước: Speech Recognition -> Translation -> Speech Synthesis.
- Ví dụ: Tạo một `Custom Chain` kế thừa từ `Chain` class của Langchain, trong đó mỗi bước của pipeline là một mắt xích.
- Sử dụng Langchain để quản lý prompt nếu cần thêm các tác vụ xử lý ngôn ngữ tự nhiên phức tạp hơn (ví dụ: tóm tắt, điều chỉnh văn phong).

### 5. **PyTorch (Nền tảng cho Model)**

- Khi làm việc với các model từ Hugging Face, hãy đảm bảo code tương thích với PyTorch.
- Tối ưu hóa hiệu năng:
    - Chuyển model và tensor sang GPU (`.to('cuda')`) nếu có thể để tăng tốc xử lý.
    - Sử dụng `torch.no_grad()` trong quá trình inference để giảm bộ nhớ và tăng tốc độ.
- Quản lý tài nguyên tensor một cách cẩn thận để tránh rò rỉ bộ nhớ trên GPU.