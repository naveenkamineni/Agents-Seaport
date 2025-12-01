from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph
import asyncio


class AgentState(TypedDict):
    file_path : str
    content : str
    value1 : int
    value2 : int 
    messages : list[HumanMessage, SystemMessage]
     
llm = ChatOpenAI(model="gpt-4o-mini")
 
@tool   
def add_two_numbers(state : AgentState) -> AgentState:
    """ Use this function to add two numbers"""
    return f" {state["value1"]} + {state["value2"]} = {state["value1"] + state["value2"]}"

@tool
def read_files(state: AgentState) -> AgentState:
    """Use this Function to read files that tell you about Naveen Recommendation for Abroad Education"""
    try:
        with open(state["file_path"], 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return f"File not found: {state['file_path']}"

file_path = r"C:\Users\DELL\OneDrive\Desktop\Cyient.txt"

tools = [add_two_numbers, read_files]

agent = create_agent(llm, tools)

#user_input = input("Enter your query: ")
response = agent.invoke({"messages":[SystemMessage(content="You are a helpful assistent Agent ."), 
                                     HumanMessage(content=f"Here is the file path: {file_path}. What do you know about Naveen Recommendation?")]})


print("Final Answer:")
print(response["messages"][-1].content)


