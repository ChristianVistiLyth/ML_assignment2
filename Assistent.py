
import asyncio
import os

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

SYSTEM_PROMPT = """\
You are a research-paper assistant. The user will describe the kind of
academic paper they are looking for
"""


async def main():
    client = OpenAIChatCompletionClient(
        model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        api_key=os.getenv("KEY"),
    )

    agent = AssistantAgent(
        name="ResearchAgent",
        model_client=client,
        system_message=SYSTEM_PROMPT,
    )

    print("Research Agent ready. Type 'quit' to exit.\n")

    while True:
        try:
            query = input("You ▸ ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not query or query.lower() in {"quit", "exit", "q"}:
            break

        response = await agent.on_messages(
            [TextMessage(content=query, source="user")],
            cancellation_token=CancellationToken(),
        )
        print(f"\nAgent ▸ {response.chat_message.content}\n")


if __name__ == "__main__":
    asyncio.run(main())