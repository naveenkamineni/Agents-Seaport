import subprocess
from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    command: str
    content: str

def state1(state: AgentState) -> AgentState:
    result = subprocess.run(state["command"], 
        shell=True,
        capture_output=True,
        text=True )
    state["content"] = result.stdout or result.stderr
    return state

# Build the workflow
workflow = StateGraph(AgentState)
workflow.add_node("state1", state1)

workflow.set_entry_point("state1")
workflow.set_finish_point("state1")  # since we’re not looping

graph = workflow.compile()

# Get input and run
user_command = input("Enter the file path to read: ")

initial_state: AgentState = {
    "command": user_command,
    "content": ""
}

compiled = graph.invoke(initial_state)

print(f"\nFile Content:\n{compiled['content']}")
