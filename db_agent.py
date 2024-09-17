
from pprint import pprint as pp
import os

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_google_vertexai import ChatVertexAI

from sqlalchemy import *
from sqlalchemy.schema import *
from sqlalchemy.dialects import registry

import order
import config as c


PROJECT = c.BQ_PROJECT
DATASET = c.BQ_DATASET
TABLE = c.BQ_TABLE

# try Spanner
SPANNER_DATABASE = c.SPANNER_DATABASE
SPANNER_INSTANCE = c.SPANNER_INSTANCE

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
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

def ask_agent(content: str = order.message):
    print("sqlalchemy_url:", sqlalchemy_url)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type="zero-shot-react-description", # https://api.python.langchain.com/en/latest/agents/langchain.agents.agent_types.AgentType.html#langchain.agents.agent_types.AgentType
        use_query_checker=True,
        # top_k=1,
        verbose=DEBUG,
    )

    data = agent_executor.invoke(content)

    return data["output"]

if __name__ == "__main__":

    import sys
    content = ""
    if len(sys.argv) > 2:
        content = sys.argv[1]
    ask_agent(content)

