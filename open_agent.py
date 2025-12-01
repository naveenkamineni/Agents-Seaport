# required libraries
# pip install langchain(Version: 1.0.5) langchain_openai(Version: 1.0.2) langchain_core(Version: 1.0.4)

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
import requests

# intialize the LLM
llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0)

# Define a custom tool for time retrieval
@tool
def get_current_time() -> str:
    """Get the current time in HH:MM:SS format."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

Test_API_URL = "https://17h28vj084.execute-api.ap-south-1.amazonaws.com/agent"

@tool
def call_test_apigateway(query: str) -> str:
    """Calls the AWS API Gateway Lambda endpoint using GET."""
    try:
        response = requests.get(Test_API_URL, params={"query": query})
        return response.text
    except Exception as e:
        return f"Error calling API: {e}"

Resource_API_URL = "https://a6vh0nqfa6.execute-api.ap-south-1.amazonaws.com/default/Aws_Resource_Manager"

@tool
def call_ec2_instance(query: str) -> str:
    """Call this Function to know the AWS Ec2 Instance details./ Instance:{Running, Stopped, Terminated}"""
    try:
        response = requests.get(Resource_API_URL, params={"query": query})
        return response.text
    except Exception as e:
        return f"Error calling API: {e}"
    
# Add tool to the toolkit
tools = [get_current_time, call_test_apigateway, call_ec2_instance]

# Create the agent with the LLM and tools
agent = create_agent(llm, tools)

# Invoke the agent with a user query
response = agent.invoke({"messages":[SystemMessage(content="You are a helpful assistent Agent ."), 
                                     HumanMessage(content="test aws api-gateway") ]})

# Process the response
print("Final Answer:")
print(response["messages"][-1].content)
