import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from .config import DATABASE_URL, DATA_DIR


def get_engine() -> Engine:
	return create_engine(DATABASE_URL, future=True)


def sanitize_table_name(filename: str) -> str:
	name = Path(filename).stem
	name = name.lower().replace(" ", "_").replace("-", "_")
	# Remove characters not allowed in SQL table names
	allowed = "abcdefghijklmnopqrstuvwxyz0123456789_"
	name = "".join(ch for ch in name if ch in allowed)
	if not name:
		name = "table"
	return name


def load_excel_to_sqlite(excel_path: str, engine: Engine, if_exists: str = "replace") -> str:
	"""Load a single Excel file to SQLite as a table and return the table name."""
	df = pd.read_excel(excel_path)
	table_name = sanitize_table_name(os.path.basename(excel_path))
	df.to_sql(table_name, engine, if_exists=if_exists, index=False)
	return table_name


def auto_load_directory(directory: str | None = None) -> list[str]:
	"""Load all .xlsx files in a directory to the configured database. Returns table names."""
	directory = directory or DATA_DIR
	engine = get_engine()
	created_tables: list[str] = []
	for entry in os.listdir(directory):
		if entry.lower().endswith(".xlsx"):
			path = os.path.join(directory, entry)
			table = load_excel_to_sqlite(path, engine)
			created_tables.append(table)
	return created_tables


def list_tables(engine: Engine | None = None) -> list[str]:
	engine = engine or get_engine()
	with engine.connect() as conn:
		rows = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")).fetchall()
	return [r[0] for r in rows]


if __name__ == "__main__":
	eng = get_engine()
	tables = auto_load_directory()
	print("Loaded tables:", tables)
	print("All tables in DB:", list_tables(eng))
