import re
from pathlib import Path
from typing import List, Tuple, Optional

import pandas as pd
from sqlalchemy import create_engine, text, inspect

import psycopg2


DB_CONFIG = {
    "name": "gia_example",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": "5432",
}


def get_conn_url(db_name: Optional[str] = None) -> str:
    base = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}"
    return f"{base}/{db_name or 'postgres'}"


def ensure_database_exists():
    engine = create_engine(
        get_conn_url("postgres"),
        isolation_level="AUTOCOMMIT",
    )
    db_name = DB_CONFIG["name"]
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": db_name},
        )
        if result.scalar():
            print(f"ℹ️ База данных '{db_name}' уже существует.")
        else:
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f"✅ База данных '{db_name}' создана.")


def get_table_names(engine) -> List[str]:
    inspector = inspect(engine)
    return inspector.get_table_names()


def snake_case(name: str) -> str:
    name = re.sub(r"[\s\-\.]+", "_", name)
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower().replace(".xlsx", "").replace(".csv", "")


def import_xlsx_files_if_needed():
    db_url = get_conn_url(DB_CONFIG["name"])
    engine = create_engine(db_url)

    existing_tables = set(get_table_names(engine))
    xlsx_files = list(Path("./data").glob("*.xlsx"))

    if not xlsx_files:
        print("⚠️ Нет .xlsx файлов для импорта.")
        return

    new_tables = False
    for xlsx_path in xlsx_files:
        table_name = snake_case(xlsx_path.name)
        if not re.fullmatch(r"[a-z_][a-z0-9_]*", table_name):
            print(
                f"❌ Некорректное имя таблицы из файла: {xlsx_path.name} → {table_name}"
            )
            continue

        if table_name not in existing_tables:
            print(f"📥 Импорт {xlsx_path.name} → таблица '{table_name}'")
            df = pd.read_excel(xlsx_path, dtype=str)
            df.columns = df.columns.str.strip()
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists="replace",
                index=False,
                method="multi",
                chunksize=1000,
            )
            new_tables = True
            print(f"✅ Загружено {len(df)} строк в '{table_name}'")

    if not new_tables:
        print("ℹ️ Все таблицы уже существуют. Импорт не требуется.")


def get_table_data(table_name: str) -> Tuple[List[str], List[tuple]]:
    if not re.fullmatch(r"[a-z_][a-z0-9_]*", table_name):
        raise ValueError("Недопустимое имя таблицы")

    conn = psycopg2.connect(
        dbname=DB_CONFIG["name"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
    )
    try:
        with conn.cursor() as cur:
            cur.execute(f'SELECT * FROM "{table_name}"')
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
        return columns, rows
    finally:
        conn.close()
