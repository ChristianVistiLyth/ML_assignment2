
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

SYSTEM_PROMPT = f"""\
You help researchers find academic papers on {PROVIDER}.

Your tool: search_papers(topic, year_min, year_max, min_citations, max_citations, limit).
It returns JSON with title, authors, year, citation_count, url, and abstract.

For every request:

Thought: Identify the topic, year range, citation thresholds, and number of
results the user asked for. Use those exact constraints - do not relax them.

Action: Call search_papers once with arguments that match the request literally.

Observation: Read the JSON.

Final Answer: List only the papers the tool returned that match every
constraint. For each: title, authors, year, citation count, URL, and one
sentence based on the abstract. If the tool returns no matching papers, say
so and stop. Do not suggest alternatives, do not broaden the search,
do not retry with looser filters.

Hard rules:
- Never invent or guess papers, authors, years, or citations.
- Never recommend a paper that is not in the tool output.
- Never loosen the user's filters. If nothing matches, return nothing.
"""

config_list = [
    {
        "api_type": "mistral",
        "model": os.getenv("MODEL_NAME", "mistral-small-latest"),
        "api_key": os.getenv("MISTRAL_API_KEY"),
    }
]

assistant = autogen.AssistantAgent(
    name="ResearchAgent",
    system_message=SYSTEM_PROMPT,
    llm_config={"config_list": config_list},
)

user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=5,
    code_execution_config=False,
)

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
    return search_papers(topic, year_min, year_max, min_citations, max_citations, limit)


if __name__ == "__main__":
    print("Research Agent ready. Type 'quit' to exit.\n")
    user_proxy.initiate_chat(assistant, message=input("You ▸ ").strip())
