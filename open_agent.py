# required libraries
# pip install langchain(Version: 1.0.5) langchain_openai(Version: 1.0.2) langchain_core(Version: 1.0.4)

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

# intialize the LLM
llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0)

# Define a custom tool for time retrieval
@tool
def get_current_time() -> str:
    """Get the current time in HH:MM:SS format."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

# Add tool to the toolkit
tools = [get_current_time]

# Create the agent with the LLM and tools
agent = create_agent(llm, tools)

# Invoke the agent with a user query
response = agent.invoke({"messages":[SystemMessage(content="You are a helpful assistent Agent ."), HumanMessage(content="What is the current time?")]})

# Process the response
print("Agent Response:")
print(response["messages"])
print("Final Answer:")
print(response["messages"][-1].content)
