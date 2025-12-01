from agents import Agent, Runner

# ---------------------------------------
# Agents
# ---------------------------------------
technical_agent = Agent(
    model="gpt-4o-mini",
    handoff_instructions="If the user's question is related to math, please hand off the conversation to the math tutor.",
    instructions="You are a technical assistant that provides detailed explanations on programming topics."
)

math_tutor = Agent(
    model="gpt-4o-mini",
    handoff_instructions="If the user's question is not related to math, please hand off the conversation to the technical assistant.",
    instructions="You are a math tutor that helps students understand mathematical concepts clearly."
)

commander_agent = Agent(
    model="gpt-4o-mini",
    instructions="You are a commander agent that routes user queries to either the technical assistant or the math tutor based on the topic.",
    agents=[technical_agent, math_tutor]
)

runner = Runner(agent=commander_agent)

# ---------------------------------------
# Logging (fixed)
# ---------------------------------------
def print_message_log(user_input, response, runner):
    print("\n==== Conversation Trace ====\n")

    # Which agent actually responded?
    active = getattr(runner.agent, "active_agent", None)
    agent_name = active.name if active else "unknown"

    print(f"[Agent: {agent_name}]")

    # Human message
    print("\n[Message Type: HUMAN]")
    print(user_input)

    # AI message (response is a string)
    print("\n[Message Type: AI]")
    print(response)

    print("\n============================\n")


# ---------------------------------------
# Execute
# ---------------------------------------
user_input = input("Enter your question: ")

response = Runner.run(user_input)

#print_message_log(user_input, response, runner)

print("Agent Response:", response)
