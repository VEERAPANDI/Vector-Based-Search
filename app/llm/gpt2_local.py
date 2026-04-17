from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

MODEL_PATH = "app/models/gpt2"

tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)
model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)
model.eval()

# 🔴 IMPORTANT FIX
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.eos_token_id

def gpt2_generate(prompt: str, max_new_tokens: int = 80):
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    with torch.no_grad():
        output = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )

    return tokenizer.decode(output[0], skip_special_tokens=True)
