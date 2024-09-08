
from pprint import pprint as pp
import os

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_google_vertexai import ChatVertexAI

from sqlalchemy import *
from sqlalchemy.schema import *
from sqlalchemy.dialects import registry

PROJECT = os.environ.get("PROJECT_ID")
DATASET = os.environ.get("DATASET_ID", "my_dataset")
TABLE = os.environ.get("TABLE_ID", "spanner_analysis")
DEBUG = "DEBUG" in os.environ

sqlalchemy_url = f'bigquery://{PROJECT}/{DATASET}'

registry.register('bigquery', 'sqlalchemy_bigquery', 'BigQueryDialect')

llm = ChatVertexAI(
    model="gemini-1.5-flash-001",
    temperature=1.0,
    max_tokens=None,
    max_retries=6,
    stop=None,
    # other params...
)


db = SQLDatabase.from_uri(sqlalchemy_url)
# llm = OpenAI(temperature=0, model="text-davinci-003")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type="zero-shot-react-description", # https://api.python.langchain.com/en/latest/agents/langchain.agents.agent_types.AgentType.html#langchain.agents.agent_types.AgentType
    use_query_checker=True,
    # top_k=1,
    verbose=DEBUG,
)

# 料金が1000円以下でcreated_atが2000年以前のアイテムを出して
# 料金が1000円以下のアイテムを出して
data = agent_executor.invoke("""
料金が1000円以上、1200円以下でcreated_atが2000年移行のアイテムとその料金と作成日を抽出して、料金の安い順に昇順で出して
結果はmarkdownの表形式で出力して
""")

print(data["output"])
