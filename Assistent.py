
import os

from dotenv import load_dotenv
import autogen
from autogen.oai.mistral import MistralAIClient

load_dotenv()

SYSTEM_PROMPT = """\
You are a research-paper assistant. The user will describe the kind of
academic paper they are looking for
"""

config_list = [
    {
        "model": os.getenv("MODEL_NAME", "mistral-small-latest"),
        "api_key": os.getenv("MISTRAL_API_KEY"),
        "model_client_cls": "MistralAIClient",
    }
]

autogen.AssistantAgent.register_model_client(model_client_cls=MistralAIClient)

assistant = autogen.AssistantAgent(
    name="ResearchAgent",
    system_message=SYSTEM_PROMPT,
    llm_config={"config_list": config_list},
)

user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=0,
    code_execution_config=False,
)

if __name__ == "__main__":
    print("Research Agent ready. Type 'quit' to exit.\n")
    user_proxy.initiate_chat(assistant, message=input("You ▸ ").strip())
