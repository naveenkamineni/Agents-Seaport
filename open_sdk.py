from openai import AsyncOpenAI
from agents import Agent, Runner, set_default_openai_client, SQLiteSession

client = AsyncOpenAI()
set_default_openai_client(client, use_for_tracing=True)

assistant = Agent(
    name="Helpful Assistant",
    model="gpt-4o-mini",
    instructions="You are a helpful bot.",
)

session = SQLiteSession("conversation_123")

async def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the assistant. Goodbye!")
            break
        else:
            result = await Runner.run(
                assistant,
                user_input,
                session=session
            )

            print(result.final_output)  # only print the answer text

import asyncio
asyncio.run(main())
