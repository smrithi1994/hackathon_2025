import argparse
import os
from tabulate import tabulate

from src.data_loader import auto_load_directory, list_tables
from src.agent_sql import build_sql_agent, ask


def main():
	parser = argparse.ArgumentParser(description="LangChain SQL Agent over local SQLite")
	parser.add_argument("question", nargs="?", help="Natural language question to ask about the data")
	parser.add_argument("--data-dir", dest="data_dir", default=None, help="Directory containing Excel .xlsx files")
	parser.add_argument("--no-load", dest="no_load", action="store_true", help="Skip loading data from directory")
	args = parser.parse_args()

	if not args.no_load:
		created = auto_load_directory(args.data_dir)
		if created:
			print("Loaded tables:", created)
		else:
			print("No .xlsx files found or loaded.")

	print("Tables in DB:", list_tables())

	agent = build_sql_agent()

	if args.question:
		result = ask(agent, args.question)
		print("\nAnswer:")
		print(result["answer"])
	else:
		print("\nEnter questions (type 'exit' to quit):")
		while True:
			try:
				q = input("> ").strip()
			except (EOFError, KeyboardInterrupt):
				break
			if not q or q.lower() in {"exit", "quit", "q"}:
				break
			res = ask(agent, q)
			print(res["answer"]) 


if __name__ == "__main__":
	main()
