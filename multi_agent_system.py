from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph
from openai import OpenAI
from langchain_openai import ChatOpenAI

# Initialize the OpenAI client
client = OpenAI()

# Define our message types
class AgentState(TypedDict):
    messages: List[BaseMessage]

# Create our agents using OpenAI
planner = ChatOpenAI(model="gpt-4", temperature=0)
executor = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define agent nodes
def task_planner(state: AgentState) -> AgentState:
    """Planning agent that breaks down tasks into subtasks."""
    messages = state["messages"]
    
    # Get the latest human message
    human_message = [m for m in messages if isinstance(m, HumanMessage)][-1]
    
    # Create the planning prompt
    planning_prompt = f"""You are a task planning agent. Break down the following task into smaller, actionable subtasks:
    
    Task: {human_message.content}
    
    Provide a numbered list of subtasks."""
    
    # Get response from OpenAI
    response = planner.invoke([HumanMessage(content=planning_prompt)])
    
    # Update the conversation with the plan
    new_messages = list(messages) + [
        AIMessage(content=f"Task Planner: {response.content}")
    ]
    
    return {"messages": new_messages}

def task_executor(state: AgentState) -> AgentState:
    """Execution agent that processes subtasks."""
    messages = state["messages"]
    
    # Get the latest plan
    planner_message = [m for m in messages if isinstance(m, AIMessage)][-1]
    
    # Create the execution prompt
    execution_prompt = f"""You are a task execution agent. Based on the following plan, provide specific steps or actions for implementation:
    
    Plan: {planner_message.content}
    
    Provide detailed implementation steps."""
    
    # Get response from OpenAI
    response = executor.invoke([HumanMessage(content=execution_prompt)])
    
    # Update the conversation with the execution details
    new_messages = list(messages) + [
        AIMessage(content=f"Task Executor: {response.content}")
    ]
    
    return {"messages": new_messages}

# Remove the should_continue function as it's no longer needed

# Define the workflow graph
def build_graph():
    # Create a new graph
    workflow = StateGraph(AgentState)
    
    # Add our agents as nodes
    workflow.add_node("planner", task_planner)
    workflow.add_node("executor", task_executor)
    
    # Add conditional edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")
    
    # End the graph with the executor
    workflow.set_finish_point("executor")
    
    return workflow

# Create an interface to run the system
def run_agent_system(task: str):
    # Initialize the graph
    graph = build_graph()
    
    # Compile the graph into a runnable chain
    app = graph.compile()
    
    # Prepare the initial state
    initial_state = {
        "messages": [HumanMessage(content=task)]
    }
    
    # Run the system
    result = app.invoke(initial_state)
    
    # Print the conversation
    for message in result["messages"]:
        if isinstance(message, HumanMessage):
            print(f"\nHuman: {message.content}")
        elif isinstance(message, AIMessage):
            print(f"\n{message.content}")

# Example usage
if __name__ == "__main__":
    task = "Design a database schema for an e-commerce platform"
    run_agent_system(task)