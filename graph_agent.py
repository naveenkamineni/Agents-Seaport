from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
import os

# Make sure your API key is set in the environment before running this script:
# export OPENAI_API_KEY="your-key"

# 1️⃣ Define the Agent State using TypedDict (not a function)
class AgentState(TypedDict):
    messages: List[HumanMessage]

# 2️⃣ Initialize the LLM
llm = ChatOpenAI(model="gpt-4o")

# 3️⃣ Define your process node
def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print("Response:", response.content)
    # Return updated state (must include messages again)
    return state

# 4️⃣ Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("process", process)
workflow.add_edge(START, "process")
workflow.add_edge("process", END)
graph = workflow.compile()

# 5️⃣ Run with user input
result = graph.invoke({"messages": [HumanMessage(content=["hii","what is the time Now in Los Anglos"])]})
