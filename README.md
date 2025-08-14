# Real-Time Voice Translation

This project provides real-time voice translation using state-of-the-art AI models for speech-to-text, translation, and text-to-speech.

## Features
- Speech recognition (AssemblyAI)
- Translation (Google Gemini, OpenAI, HuggingFace)
- Text-to-speech (ElevenLabs, Suno Bark)
- Easy configuration via `.env` file

## Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/Key9x98/real-time-voice-translation.git
   ```
2. Create and activate a Python virtual environment:
   ```sh
   python -m venv venv-speechtospeech
   venv-speechtospeech\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Add your API keys to the `.env` file (see example in repo).

## Usage
- Run `gemini_model.py` for translation using Gemini API.
- Run `voice_model.py` for text-to-speech demo.
- See `model.py` for HuggingFace translation example.

## Notes
- Do **not** commit your `.env` file or virtual environment folders.
- See `.gitignore` for excluded files.

## License
MIT
