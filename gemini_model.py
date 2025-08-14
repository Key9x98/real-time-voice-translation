from transformers import AutoTokenizer, AutoModelForCausalLM
from openai import OpenAI
import os
from dotenv import load_dotenv


class GeminiTranslator:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/",
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def translate(
        self,
        sentence: str,
        language: str = "Vietnamese",
        model: str = "gemini-2.5-flash",
    ) -> str:
        system_prompt = f"You are a helpful assistant. Translate the following sentence into {{language}}, return ONLY the translation, nothing else. Sentence: {{sentence}}"
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Translate the following English sentence into {language}:\n{sentence} <vi>",
            },
        ]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    translator = GeminiTranslator(api_key)
    sentence = input("Enter a sentence in English to translate: ")
    language = "Vietnamese"
    translation = translator.translate(sentence, language)
    print(translation)
