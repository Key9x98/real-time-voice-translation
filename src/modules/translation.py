# Translation module
# Implement HuggingFace or Gemini translation logic here


from openai import OpenAI
from src.core.config import ProjectConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class GeminiTranslator:
    def __init__(
        self, base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    ):
        config = ProjectConfig()
        self.api_key = config.get("GEMINI_API_KEY")
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)

    def translate(self, sentence: str, language: str = None, model: str = None) -> str:
        config = ProjectConfig()
        language = language or config.get("LANGUAGES", {}).get("target", "Vietnamese")
        model = model or config.get("gemini-2.5-flash", default="gemini-2.5-flash")
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


def demo_translate():
    translator = GeminiTranslator()
    sentence = "You are my sunshine"
    config = ProjectConfig()
    language = config.get("LANGUAGES", {}).get("target", "Vietnamese")
    translation = translator.translate(sentence, language)
    print(translation)


def hf_translate_example():
    config = ProjectConfig()
    model_name = config.get("TRANSLATION_MODEL", "unsloth/Qwen2.5-1.5B")

    # Load tokenizer & model từ cùng nguồn, set pad_token nếu thiếu
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.to("cuda" if torch.cuda.is_available() else "cpu")

    vocab_size = model.config.vocab_size
    print("Vocab size:", vocab_size)

    messages = [
        "Translate the following English sentence into Vietnamese:\nYou are my sunshine <vi>"
    ]
    for message in messages:
        inputs = tokenizer(
            message, return_tensors="pt", max_length=256, padding=True, truncation=True
        ).to(model.device)

        print("Max token ID:", inputs["input_ids"].max().item())

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )

        # Bỏ phần prompt khỏi output
        generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]
        response = tokenizer.decode(generated_tokens, skip_special_tokens=True)
        print(response.strip())
		
        # Lấy phần giữa <vi>...</vi>
        if "<vi>" in response:
            response = response.split("<vi>", 1)[1]
        if "</vi>" in response:
            response = response.split("</vi>", 1)[0]

        print(response.strip())



if __name__ == "__main__":
    demo_translate()
    # Uncomment the line below to test HuggingFace translation
    hf_translate_example()
