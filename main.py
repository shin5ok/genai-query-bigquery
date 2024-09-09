
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

# try Spanner
SPANNER_INSTANCE = os.environ.get("SPANNER_INSTANCE_ID")
SPANNER_DATABASE = os.environ.get("SPANNER_DATABASE_ID")

DEBUG = "DEBUG" in os.environ

sqlalchemy_url = f'bigquery://{PROJECT}/{DATASET}'
if SPANNER_INSTANCE and SPANNER_DATABASE:
    sqlalchemy_url = f'spanner+spanner:///projects/{PROJECT}/instances/{SPANNER_INSTANCE}/databases/{SPANNER_DATABASE}'

# Initializing...
registry.register('bigquery', 'sqlalchemy_bigquery', 'BigQueryDialect')
registry.register('spanner', 'google.cloud.sqlalchemy_spanner', 'SpannerDialect')

llm = ChatVertexAI(
    model="gemini-1.5-flash-001",
    temperature=0,
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

import order
data = agent_executor.invoke(order.message)

print(data["output"])
