# ML Assignment 2 — Research Paper Agent

## Setup

Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Dependency Installation

```powershell
pip install -r requirements.txt
```

## API Key Configuration

Copy the example env file and fill in your keys:

```powershell
Copy-Item .env.example .env
```

Then open `.env` and replace the placeholders:

```
MISTRAL_API_KEY=your_mistral_key_here
SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_key_here  # optional, but increases rate limits
```

Get a Mistral API key at [console.mistral.ai](https://console.mistral.ai).

## How to Run

```powershell
python Assistant.py
```

The agent will prompt you to describe what kind of papers you are looking for. Type your request and press Enter. Type `quit` to exit.

## Evaluation Results

read eval.md for more info

## Group Member Contributions

- Christian built `Assistant.py` — agent setup, LLM configuration, and the conversation call flow.
- Anders built `tools.py` — Semantic Scholar API integration, and ran evaluation on 10 prompts.


## Reflection

What worked well?
Pretty easy to use the mistral model

What failed or was unreliable?
Package version of the api ofen has version issues.

How often did the agent need tool calls?
only ones at startup.

Did the LLM ever hallucinate?
no but we had short context. maybe if we made some longer conversations it would.

How did you prevent incorrect answers?
by making the system prompt as specific as posssible

What would you improve with more time?
more test cases with different scenaries. maybe a better/paid model.