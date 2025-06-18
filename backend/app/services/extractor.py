from llama_cpp import Llama
import os
import json
import re
import time

MODEL_PATH = os.getenv("LLAMA_MODEL", "/app/models/llama-7b.gguf")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    n_batch=128  # ⏱ критично для скорости!
)

EXTRACTION_PROMPT = """
Ты — помощник валютного контроля. Проанализируй текст внешнеэкономического договора и верни следующие параметры в формате JSON:

{
  "contract_number": "номер договора",
  "contract_date": "дата договора в формате YYYY-MM-DD",
  "contract_amount": "сумма договора (число)",
  "currency": "валюта (например, USD)",
  "deal_type": "экспорт или импорт",
  "tnved_code": "ТН ВЭД код (если есть)",
  "foreign_partner": {
    "name": "название контрагента",
    "country": "страна",
    "swift": "SWIFT-код (если есть)",
    "address": "адрес"
  },
  "payment_terms": "условия оплаты (если есть)"
}

🔒 ВАЖНО: Верни только корректный JSON, без пояснений. Начни ответ с символа `{`. Если не можешь извлечь — верни {"error": "failed"}.

Текст:
"""

def extract_contract_parameters(text: str) -> dict:
    print("🧠 [LLM] Извлечение параметров договора...")
    start = time.time()

    # Ограничим объём контекста для скорости и релевантности
    context = text[:1500].strip()
    prompt = EXTRACTION_PROMPT + context

    result = llm(prompt, stop=["\n\n"], temperature=0.2)
    output = result["choices"][0]["text"].strip()

    print(f"⏱️ [LLM] Время инференса: {time.time() - start:.2f} сек")
    print(f"📥 [LLM-ответ] {output[:200]}...")

    try:
        match = re.search(r"{.*}", output, re.DOTALL)
        if not match:
            raise ValueError("Ответ не содержит JSON-блока")
        parsed = json.loads(match.group(0))
        if "error" in parsed:
            raise ValueError("LLM вернула ошибку: failed")
        return parsed
    except Exception as e:
        raise ValueError(f"Ошибка при парсинге JSON из LLM: {str(e)}\nОтвет: {output}")
