
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("unsloth/Qwen2.5-1.5B")
model = AutoModelForCausalLM.from_pretrained("unsloth/Qwen2.5-1.5B")

messages = [
    "Translate the following English sentence into Chinese:\nMay the force be with you <zh>",
    "Translate the following English sentence into Chinese and explain it in detail:\nMay the force be with you <zh>"
]

responses = []
for message in messages:
    inputs = tokenizer(message, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=512)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    responses.append(response.strip())

print(responses)
