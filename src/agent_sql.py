from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_core.callbacks import CallbackManagerForToolRun

from .config import DATABASE_URL, OPENAI_API_KEY, OPENAI_MODEL


def get_llm(api_key: Optional[str] = None, model: Optional[str] = None):
	api_key = api_key or OPENAI_API_KEY
	model = model or OPENAI_MODEL
	if not api_key:
		raise RuntimeError("OPENAI_API_KEY not set. Provide it in environment or .env")
	return ChatOpenAI(api_key=api_key, model=model, temperature=0)


def get_db() -> SQLDatabase:
	return SQLDatabase.from_uri(DATABASE_URL)


def build_sql_agent():
	llm = get_llm()
	db = get_db()
	agent_executor = create_sql_agent(
		llm=llm,
		db=db,
		verbose=False,
	)
	return agent_executor


def ask(agent, question: str) -> dict:
	"""Run a question through the SQL agent. Returns dict with sql and result."""
	response = agent.invoke({"input": question})
	# LangChain agent returns a dict; try to extract intermediate steps if present
	final = {
		"answer": response.get("output") or response,
	}
	return final
