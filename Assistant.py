
import os
import json
import time
import requests
from typing import Annotated, Optional

from dotenv import load_dotenv
import autogen

from tools import search_papers
load_dotenv()

from tools import search_papers

load_dotenv()

PROVIDER="Semantic Scholar"

# Setup: Define the role of the LLM agent and which search service to use.
SYSTEM_PROMPT = f"""\
You are a research-paper assistant. The user will describe the kind of
academic paper they are looking for. Use the search_papers tool to find
relevant papers on Semantic {PROVIDER}
"""

# Setup: Configure which model to use and load the API key.
config_list = [
    {
        "api_type": "mistral",
        "model": os.getenv("MODEL_NAME", "mistral-small-latest"),
        "api_key": os.getenv("MISTRAL_API_KEY"),
    }
]

# Step 2 (LLM): Parse the user request. Identify constraints.
# Step 6 (LLM): Reason about relevance. Return the best matching papers.
assistant = autogen.AssistantAgent(
    name="ResearchAgent",
    system_message=SYSTEM_PROMPT,
    llm_config={"config_list": config_list},
)

# Step 7 (Deterministic): Wait for next user input after each reply.
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=5,
    code_execution_config=False,
)

# Step 3 (LLM): Ask the LLM to decide whether to call the search tool and with which parameters.
# Step 4 (Deterministic): Execute the tool call locally when the LLM decides to search.
@user_proxy.register_for_execution()
@assistant.register_for_llm(
    name="search_papers",
    description="Search {PROVIDER} for relevant papers by topic and optional year and citation filters."
)
def _search_papers(
    topic: Annotated[str, "Research topic or query string"],
    year_min: Annotated[Optional[int], "Earliest publication year"] = None,
    year_max: Annotated[Optional[int], "Latest publication year"] = None,
    min_citations: Annotated[Optional[int], "Minimum citation count"] = None,
    max_citations: Annotated[Optional[int], "Maximum citation count"] = None,
    limit: Annotated[int, "Max results (1-100)"] = 20,
) -> str:
    # Step 5 (Deterministic): Search for candidate papers. Filter candidates by year and citation count.
    return search_papers(topic, year_min, year_max, min_citations, max_citations, limit)


if __name__ == "__main__":
    # Step 1 (Deterministic): Receive the user request and start the conversation loop.
    print("Research Agent ready. Type 'quit' to exit.\n")
    user_proxy.initiate_chat(assistant, message=input("You ▸ ").strip())
