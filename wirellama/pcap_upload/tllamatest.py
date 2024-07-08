from llama_agents.launchers.local import LocalLauncher
from llama_agents.services import AgentService, ToolService
from llama_agents.tools import MetaServiceTool
from llama_agents.control_plane.server import ControlPlaneServer
from llama_agents.message_queues.simple import SimpleMessageQueue
from llama_agents.orchestrators.agent import AgentOrchestrator

from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

from IPython.display import Markdown, display
from llama_index.core import SQLDatabase
from llama_index.core import Settings
from llama_index.llms.together import TogetherLLM
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
)
from pydantic import BaseModel

import nest_asyncio

import aiofiles

async def read_message():
    async with aiofiles.open("/home/milind/linux-github/wirellama/wirellama/pcap_upload/message.txt", "r") as f:
        input = await f.read()
    return input




Settings.embed_model=None
llm = TogetherLLM(
            model="NousResearch/Nous-Hermes-2-Mistral-7B-DPO", api_key=""
        )

Settings.llm = llm

username=""
password=""
host=""
port=""
dbname=""
from llama_index.core import SQLDatabase
pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
db = SQLDatabase.from_uri(pg_uri)


engine = create_engine(pg_uri)
metadata_obj = MetaData()
sql_database = SQLDatabase(engine, include_tables=["pcap_upload_packetdata"])
print(llm.metadata)
print("")
print("")
from sqlalchemy import text

with engine.connect() as con:
    rows = con.execute(text("SELECT * from pcap_upload_packetdata limit 5"))
    for row in rows:
        print(row)
from llama_index.core.query_engine import NLSQLTableQueryEngine

Settings.embed_model=None
SQL_query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database
)


from llama_index.core.tools import QueryEngineTool, ToolMetadata


query_engine_tools = QueryEngineTool(
        query_engine=SQL_query_engine,
        metadata=ToolMetadata(
            name="sql",
            description=(
                "sql query agent: genrates sql from natural language and executes sql query on the connected database"
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    )





# create our multi-agent framework components
message_queue = SimpleMessageQueue()
tool_service = ToolService(
    message_queue=message_queue,
    tools=[query_engine_tools],
    running=True,
    step_interval=0.5,
)

control_plane = ControlPlaneServer(
    message_queue=message_queue,
    orchestrator=AgentOrchestrator(llm=OpenAI(model="gpt-3.5-turbo-0125",api_key="sk-")),
)

meta_tool = MetaServiceTool(
    tool_metadata=query_engine_tools.metadata,
    message_queue=message_queue,
    tool_service_name=tool_service.service_name,
)
worker1 = FunctionCallingAgentWorker.from_tools(
    [meta_tool],
    llm=OpenAI(model="gpt-3.5-turbo-0125",api_key="sk-"),
)
agent1 = worker1.as_agent()
agent_server_1 = AgentService(
    agent=agent1,
    message_queue=message_queue,
    description="Used to answer questions over sql database ",
    service_name="SQL_Agent",
)

# launch it
launcher = LocalLauncher(
    [agent_server_1, tool_service],
    control_plane,
    message_queue,
)
input=read_message()
print("\n \n \n ")
read_message()
print(f"Input: {input}")

with open('/home/milind/linux-github/wirellama/wirellama/pcap_upload/message.txt', 'r') as file:
    input=file.read()

result = launcher.launch_single(input)

with open("/home/milind/linux-github/wirellama/wirellama/pcap_upload/output.txt", "w") as f:
    f.write(result)
print(f"Result: {result}")
    
