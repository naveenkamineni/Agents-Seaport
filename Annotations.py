# Annotations
#1.Typed Dict
from typing import TypedDict, Union, Dict, Optional
class Person(TypedDict):
    Name: str
    age:  int
    salary : Union[int , float]
    


#2.Union:
def annotation(persons: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
    return persons

annotation({"Naveen":23, "Srinu":22.4})

#3 Optional 
name: str | None = "Jack"
another_name: Optional[str] = "Naveen"

#4. any() | all()

binary1 = [0,1,0,1]
binary2 = [0,0,0,0]
binary3 = [1,1,1,1]

#print(all(binary1)) -> False
#print(all(binary2)) -> False
#print(any(binary3)) -> True

from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    user_input: str
    response: str
    confidence: float

def collect_input(state: AgentState) -> AgentState:
    state["user_input"]
    return state

def respond(state: AgentState) -> AgentState:
    state["response"] 
    state["confidence"]
    return state

graph = StateGraph(AgentState)

graph.add_node("input", collect_input)
graph.add_node("response", respond)
graph.add_edge(START, "input")
graph.add_edge("input", "response")
graph.add_edge("response", END)

compiled = graph.compile()

result = compiled.invoke({"user_input": "Naveen", "response": "Hi There", "confidence": 100.0})
print(result)