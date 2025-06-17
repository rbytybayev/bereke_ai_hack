from llama_cpp import Llama
import os

MODEL_PATH = os.getenv("LLAMA_MODEL", "/app/models/llama-7b.gguf")
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4)

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

Ответ строго в формате JSON.

Текст:
"""

def extract_contract_parameters(text: str) -> dict:
    prompt = EXTRACTION_PROMPT + text[:4000]  # ограничим ввод для скорости
    result = llm(prompt, stop=["\n\n"], temperature=0.2)
    output = result["choices"][0]["text"].strip()

    try:
        import json
        return json.loads(output)
    except Exception as e:
        raise ValueError(f"Ошибка при парсинге JSON из LLM: {str(e)}\nОтвет: {output}")
