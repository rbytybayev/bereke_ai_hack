from llama_cpp import Llama
import os
import json
import re
import time

MODEL_PATH = os.getenv("LLAMA_MODEL", "/app/models/llama-7b.gguf")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,         # меньше контекст — быстрее
    n_threads=4,
    n_batch=128
)

PROMPT = """
Ты — помощник валютного контроля. Прочитай текст договора ниже и верни строго JSON со следующими полями:

{
  "contract_number": "...",
  "contract_date": "YYYY-MM-DD",
  "contract_amount": "...",
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

Ответ начни с символа { и верни только JSON. Никаких пояснений.
Если не можешь — верни: {"error": "failed"}

Текст:
"""

def extract_contract_parameters(text: str) -> dict:
    print("🧠 [LLM] Извлечение параметров договора...")
    start = time.time()

    context = text[:1200] + "\n\n" + text[-300:]  # начало + конец
    prompt = PROMPT + context
    print(f"🔎 [LLM prompt]: {prompt[:300]}...")

    result = llm(prompt, stop=["\n\n"], temperature=0.2)
    output = result["choices"][0]["text"].strip()

    print(f"⏱️ [LLM] Время инференса: {time.time() - start:.2f} сек")
    print(f"📥 [LLM-ответ] {output[:200]}...")

    # Поиск JSON-блока
    try:
        match = re.search(r"{.*}", output, re.DOTALL)
        if not match:
            print("⚠️ [LLM] JSON не найден, возврат ошибки.")
            return {"error": "failed"}
        data = json.loads(match.group(0))
        return data
    except Exception as e:
        print(f"🛑 [LLM] Ошибка JSON парсинга: {e}")
        return {"error": "failed"}