from llama_cpp import Llama
import os
import json
import re
import time

MODEL_PATH = os.getenv("LLAMA_MODEL", "/app/models/llama-7b.gguf")
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4, n_batch=128)

EXTRACTION_PROMPT = """
Выдели из текста договора следующие параметры в формате JSON:
- contract_number
- contract_date
- contract_amount
- currency
- deal_type (экспорт/импорт)
- tnved_code (если есть)
- foreign_partner (name, country, swift, address)
- payment_terms (если есть)

Ответ начни с символа { и верни только корректный JSON.
Если не можешь — верни {"error": "failed to extract"}.

Текст:
"""

def extract_contract_parameters(text: str) -> dict:
    print("🧠 [LLM] Извлечение параметров договора...")
    start = time.time()

    prompt = EXTRACTION_PROMPT + text[:2000]
    result = llm(prompt, stop=["\n\n"], temperature=0.2)
    output = result["choices"][0]["text"].strip()

    print(f"⏱️ [LLM] Время инференса: {time.time() - start:.2f} сек")
    print(f"📥 [LLM-ответ] {output[:200]}...")

    try:
        # Попробуем вытащить JSON фрагмент
        match = re.search(r"{.*}", output, re.DOTALL)
        if not match:
            raise ValueError("Ответ не содержит JSON-блока")
        return json.loads(match.group(0))
    except Exception as e:
        raise ValueError(f"Ошибка при парсинге JSON из LLM: {str(e)}\nОтвет: {output}")
