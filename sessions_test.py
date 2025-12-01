from agents import Agent, Runner, SQLiteSession

# Create agent
agent = Agent(
    name="Assistant",
    instructions="Reply very concisely.",
)

# Create a session instance with a session ID
session = SQLiteSession("conversation_123")

async def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the assistant. Goodbye!")
            break
        else:
            result = await Runner.run(
                agent,
                user_input,
                session=session
            )

            print(result.final_output)  # only print the answer text

import asyncio
asyncio.run(main())
