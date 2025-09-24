## LangChain SQL Agent over Excel-loaded SQLite

### Prerequisites
- Python 3.10+
- OpenAI API key

### Setup
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```
2. Create a `.env` file (copy `.env.example`) and set `OPENAI_API_KEY`.

### Data
Place your `.xlsx` files in the project root (or provide `--data-dir`). This repo includes sample files like `prime_transactions_synthetic_data_final.xlsx`.

Tables are created in a local SQLite DB at `local.db` (override with `DATABASE_URL`). Table names are derived from filenames (sanitized to lowercase underscores).

### Run
Ask a question directly:
```bash
python cli.py "What is the total amount by transaction type?"
```

Or start an interactive shell (loads data from current directory by default):
```bash
python cli.py
```

Flags:
- `--data-dir PATH`: directory to search for `.xlsx`
- `--no-load`: skip loading data (use existing DB)

### Notes
- The agent uses LangChain with OpenAI (`gpt-4o-mini`) to generate and execute SQL against SQLite.
- Ensure column names are readable; for best results, keep headers clean in Excel.
