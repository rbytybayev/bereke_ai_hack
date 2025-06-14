#!/usr/bin/env python3
import os
import sys
import time
import psycopg2
from lxml import etree

# Загружаем параметры подключения из переменных окружения
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", "5432"),
}

# Настройка путей и названия таблицы
BASE_DIR = os.getcwd()  # Рабочая директория в контейнере
XML_FILE = os.getenv(
    "DOW_JONES_XML_PATH",
    os.path.join(BASE_DIR, "app", "data", "dow_jones_data.xml")
)
TABLE_NAME = os.getenv("DOW_JONES_TABLE", "sanctions_dow_jones")


def wait_for_db(retries: int = 5, delay: int = 3):
    """
    Ожидание готовности базы данных.
    """
    print(f"Ожидание базы данных {DB_PARAMS['host']}:{DB_PARAMS['port']}...")
    for i in range(retries):
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            conn.close()
            print("База данных доступна.")
            return
        except psycopg2.OperationalError as e:
            print(f"Попытка {i+1}/{retries} не удалась ({e}). Жду {delay} секунд...")
            time.sleep(delay)
    print("Не удалось подключиться к базе данных.")
    sys.exit(1)


def create_table(conn):
    """
    Создание таблицы для загрузки санкционных списков.
    """
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id SERIAL PRIMARY KEY,
                name TEXT,
                entity_type TEXT,
                role TEXT,
                list_name TEXT,
                country TEXT,
                raw_data JSONB
            );
        """)
        conn.commit()


def insert_batch(conn, records):
    """
    Вставка пачки записей в таблицу.
    """
    with conn.cursor() as cur:
        args_str = ",".join(
            cur.mogrify("(%s, %s, %s, %s, %s, %s)", r).decode()
            for r in records
        )
        cur.execute(f"""
            INSERT INTO {TABLE_NAME} (name, entity_type, role, list_name, country, raw_data)
            VALUES {args_str};
        """)
        conn.commit()


def parse_and_insert():
    """
    Основная функция: парсинг XML и загрузка в БД.
    """
    # 1. Ждём готовности БД
    wait_for_db()

    # 2. Подключаемся и создаём таблицу
    conn = psycopg2.connect(**DB_PARAMS)
    create_table(conn)

    # 3. Проверяем наличие XML-файла
    if not os.path.exists(XML_FILE):
        print(f"XML-файл не найден по пути: {XML_FILE}")
        sys.exit(1)

    # 4. Итеративный парсинг и сбор данных
    print(f"Начало парсинга {XML_FILE}")
    context = etree.iterparse(XML_FILE, events=('end',), tag='Entity')
    batch = []
    for _, elem in context:
        name = elem.findtext('Name') or ''
        entity_type = elem.findtext('EntityType') or ''
        role = elem.findtext('Role') or ''
        list_name = elem.findtext('List') or ''
        country = elem.findtext('Country') or ''
        raw = {child.tag: child.text for child in elem.iterchildren()}

        batch.append((name, entity_type, role, list_name, country, raw))
        if len(batch) >= 100:
            insert_batch(conn, batch)
            batch.clear()
        elem.clear()

    # 5. Сохраняем остаток
    if batch:
        insert_batch(conn, batch)
    conn.close()
    print("Загрузка завершена.")


if __name__ == "__main__":
    parse_and_insert()
