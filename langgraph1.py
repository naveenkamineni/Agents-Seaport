from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

# 1️⃣ Define the state
class AgentState(TypedDict):
    messages: List[HumanMessage]
    input: str

# 2️⃣ Initialize model once
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3️⃣ Define node function
def chat(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    # Add the AI's message to the conversation
    state["messages"].append(AIMessage(content=response.content))
    return state

# 4️⃣ Build the workflow
workflow = StateGraph(AgentState)
workflow.add_node("process", chat)
workflow.add_edge(START, "process")
workflow.add_edge("process", END)

graph = workflow.compile()

# 5️⃣ Run with user input
result = graph.invoke({
    "messages": [HumanMessage(content="Hi, what is the time now in Los Angeles?")],
    "input": "Get time in Los Angeles"
})

# 6️⃣ Show result
for msg in result["messages"]:
    print(f"{msg.type.upper()}: {msg.content}")
