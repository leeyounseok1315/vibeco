import os
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool

@tool
def add(a: int, b: int) -> int:
    """두 숫자를 더합니다."""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """두 숫자를 뺍니다."""
    return a - b

tools = [add, subtract]

llm = ChatOpenAI(model="gpt-4o", temperature=0)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

response = agent.invoke("7에서 3을 빼줘")

print("응답:", response)

