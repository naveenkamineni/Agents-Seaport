from agents import Agent, Runner

# Create an agent with instructions
agent = Agent(
    model="gpt-4o-mini",
    instructions="You are a helpful assistant that explains technical concepts in simple words."
)

# Create a runner to execute the agent
runner = Runner(agent=agent)

# Run the agent with a query
response = runner.run("Explain what mcp is in simple words.")

print("Agent Response:", response)

    