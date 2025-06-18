from llama_cpp import Llama
import os
import json

MODEL_PATH = os.getenv("LLAMA_MODEL", "/app/models/llama-7b.gguf")
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4, n_batch=128)

SUMMARY_PROMPT = """
На основе следующих результатов проверки валютного договора сформируй краткое объяснение для клиента. Укажи, какие критерии не были пройдены и почему. Используй деловой стиль и пиши на русском языке. В конце сделай однозначный вывод: Принять или Отказать.

Результаты проверок:
{checks_json}
"""

def generate_summary_and_verdict(checks: list) -> dict:
    checks_json = json.dumps(checks, ensure_ascii=False, indent=2)
    prompt = SUMMARY_PROMPT.format(checks_json=checks_json)
    result = llm(prompt, stop=["\n\n"], temperature=0.2)
    output = result["choices"][0]["text"].strip()

    final_decision = "Принять" if all(c["status"] == "pass" for c in checks) else "Отказать"
    return {
        "summary": output,
        "decision": final_decision
    }
