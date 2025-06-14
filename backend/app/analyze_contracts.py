import os
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# Автоопределение пути к проекту
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Подключение к БД
DB_PARAMS = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'Ucard2025',
    'host': '94.131.81.13',
    'port': '5432'
}

def analyze_contract(contract):
    """Основная логика анализа одного договора"""
    results = []

    # Пример проверки: есть ли сумма договора
    if contract['contract_sum'] and float(contract['contract_sum']) > 0:
        results.append((contract['id'], 'amount_present', True, 'Сумма договора указана'))
    else:
        results.append((contract['id'], 'amount_present', False, 'Сумма договора не указана'))

    # Пример: проверка валюты
    if contract['currency_code'] in ('USD', 'EUR', 'KZT'):
        results.append((contract['id'], 'currency_allowed', True, f"Допустимая валюта: {contract['currency_code']}"))
    else:
        results.append((contract['id'], 'currency_allowed', False, f"Недопустимая валюта: {contract['currency_code']}"))

    # Пример: контракт с РФ
    if contract['is_rf_related']:
        results.append((contract['id'], 'rf_related', False, 'Контракт связан с РФ'))
    else:
        results.append((contract['id'], 'rf_related', True, 'Контракт не связан с РФ'))

    # Пример: санкционный риск
    if contract['is_sanction_risk']:
        results.append((contract['id'], 'sanction_check', False, 'Обнаружен санкционный риск'))
    else:
        results.append((contract['id'], 'sanction_check', True, 'Санкционный риск не выявлен'))

    # Добавить все остальные критерии по аналогии...

    return results

def main():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    # Получение всех контрактов
    cur.execute("SELECT * FROM public.contracts")
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    contracts = [dict(zip(columns, row)) for row in rows]

    all_results = []
    for contract in contracts:
        results = analyze_contract(contract)
        all_results.extend(results)

    # Сохраняем в contracts_analysis_result
    insert_query = """
    INSERT INTO public.contracts_analysis_result
        (contract_id, criterion_code, passed, comment)
    VALUES %s
    ON CONFLICT (contract_id, criterion_code)
    DO UPDATE SET passed = excluded.passed, comment = excluded.comment;
    """

    execute_values(cur, insert_query, all_results)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Анализ завершён и результаты сохранены.")

if __name__ == '__main__':
    main()
