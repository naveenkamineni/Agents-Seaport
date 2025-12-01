from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1️⃣ Define the state
class AgentState(TypedDict):
    messages: str
    x: list[int]
 
def stage1(state: AgentState) -> AgentState:
    print(f"{state['messages']}")
    return state

def stage2(state: AgentState) -> AgentState:
    print(f"{state['messages']}")
    return state

def stage3(state: AgentState) -> AgentState:
    print(f"{state['messages']}, x sum: {sum(state['x'])}")
    return state

def stage4(state: AgentState) -> AgentState:
    print(f"{state['messages']}")
    return state

def stage5(state: AgentState) -> AgentState:
    print(f"{state['messages']}")
    return state

# 3️⃣ Create the graph
graph = StateGraph(AgentState)

graph.add_node("stage1", stage1)
graph.add_node("stage2", stage2)
graph.add_node("stage3", stage3)
graph.add_node("stage4", stage4)
graph.add_node("stage5", stage5)

# 4️⃣ Define flow between nodes
graph.set_entry_point("stage1")
graph.add_edge("stage1", "stage2")
graph.add_edge("stage2", "stage3")
graph.add_edge("stage3", "stage4")
graph.add_edge("stage4", "stage5")
graph.add_edge("stage5", END)

# 5️⃣ Compile the graph
compiled = graph.compile()

# 6️⃣ Run the workflow
user_input = {"messages": "Start", "x": [1,2,3,4,5]}
final_state = compiled.invoke(user_input)

print("✅ Final output:")
print(final_state)
