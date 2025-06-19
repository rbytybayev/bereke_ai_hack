from llama_cpp import Llama
import os
import json
import re
import time

MODEL_PATH = os.getenv("LLAMA_MODEL", "/app/models/llama-7b.gguf")

llm = Llama(
    model_path=MODEL_PATH,  # 4-битный бинарник
    n_ctx=3064,           # или меньше, в зависимости от размера чанка
    n_threads=4,          # все ваши CPU-ядра
    n_batch=8,            # меньшие батчи – быстрее отдача
    f16_kv=True,          # хранить KV-кэш в fp16
    use_mlock=True,       # фиксировать в памяти, если есть
)

PROMPT = """
Ты — ассистент валютного контроля. 
Прочитай текст договора и верни ровно один JSON-объект по схеме:

{
  "contract_number": "...",
  "contract_date": "...",
  "contract_amount": 0.0,
  "currency": "...",
  "deal_type": "...",
  "tnved_code": "...",
  "foreign_partner": {
    "name": "...",
    "country": "...",
    "swift": "...",
    "address": "..."
  },
  "payment_terms": "..."
}

Возвращай только JSON — без пояснений, без лишних полей.  
Если не можешь извлечь — верни ровно {"error":"failed"}  
<<<END>>>

ТЕКСТ ДОГОВОРА:
"""


def chunk_text(tokens, max_len=512, overlap=64):
    for i in range(0, len(tokens), max_len - overlap):
        yield tokens[i : i + max_len]

def extract_contract_parameters(text: str) -> dict:
    print("🧠 [LLM] Извлечение параметров...")
    tokens = text.split()
    for chunk in chunk_text(tokens):
        prompt = PROMPT + " " + " ".join(chunk)
        start = time.time()
        resp = llm(
            prompt,
            stop=["<<<END>>>"],
            temperature=0.0,
            top_p=1.0,
            max_tokens=256,
        )
        duration = time.time() - start
        output = resp["choices"][0]["text"].strip()
        print(f"⏱️ {duration:.2f}s, ответ: {output[:100]}")

        m = re.search(r"(\{.*\})", output, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                continue

    return {"error": "failed"}
