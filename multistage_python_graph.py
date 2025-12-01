from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1️⃣ Define the shared state structure
class AgentState(TypedDict):
    messages: str
    x: list[int]

# 2️⃣ Define stages (nodes)
def stage1(state: AgentState) -> AgentState:
    state["messages"] = f"Hello stage1: {state['messages']}"
    state["x"] = [i * i for i in state["x"]]   # square each number
    print("➡️ stage1 output:", state)
    return state

def stage2(state: AgentState) -> AgentState:
    state["messages"] += " | stage2 done"
    state["x"].append(sum(state["x"]))          # add sum of list
    print("➡️ stage2 output:", state)
    return state

def stage3(state: AgentState) -> AgentState:
    state["messages"] += " | stage3 done"
    state["x"] = [x + 1 for x in state["x"]]    # increment all values
    print("➡️ stage3 output:", state)
    return state

def stage4(state: AgentState) -> AgentState:
    state["messages"] += " | stage4 done"
    state["x"].reverse()                        # reverse the list
    print("➡️ stage4 output:", state)
    return state

def stage5(state: AgentState) -> AgentState:
    state["messages"] += " | stage5 done ✅"
    print("➡️ stage5 output:", state)
    return state

# 3️⃣ Create the graph
graph = StateGraph(AgentState)
graph.add_node("stage1", stage1)
graph.add_node("stage2", stage2)
graph.add_node("stage3", stage3)
graph.add_node("stage4", stage4)
graph.add_node("stage5", stage5)

# 4️⃣ Define flow
graph.set_entry_point("stage1")
graph.add_edge("stage1", "stage2")
graph.add_edge("stage2", "stage3")
graph.add_edge("stage3", "stage4")
graph.add_edge("stage4", "stage5")
graph.add_edge("stage5", END)

# 5️⃣ Compile the graph
compiled = graph.compile()

# 6️⃣ Run the workflow
user_input = {"messages": "Start", "x": [1, 2, 3, 4]}
final_state = compiled.invoke(user_input)

print("\n✅ Final output:")
print(final_state)
