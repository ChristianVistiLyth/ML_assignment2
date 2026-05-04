# Agent Evaluation

## Method
Ran 10 prompts through the agent. For each prompt we recorded the answer and noted
whether it was relevant, respected year/citation constraints, gave valid
sources, avoided hallucination and explained itself.

## Tests

1. Find papers on RAG — broad topic
Answer: Returned  20 papers on RAG correctly from Semantic Scholar.
All correct topic and valid links. Summary was 1 sentence. Didn't find any fabricated entries.
# Relevant, year, no hallucination, useful.

2. Find papers using k-nearest neighbors on the MNIST handwritten digit dataset — narrow topic
Answer: Returned 10 papers all on the topic. All with valid links. Summaries from abstract.
# Relevant, year, no hallucination, useful.

3. Find 3 papers on transformers published before 2018: before year
Answer: Found 3 papers on electrical transformers, which is correctly identified not be be neural network
transformers. It correctly returned: no result, which mean it respected the constraint / rules.
# No hallucination, relevant, year, not useful. 

4. Find papers on diffusion models published after 2022: after year
Answer: Returned 3 papers all from 2023 - so year constraint respected.
# No hallucination, relevant, year, useful.

5. Find papers on attention mechanisms from 2017: exact year
Answer:

6. Find papers on reinforcement learning with at least 1000 citations: min citations
Answer:

7. Find papers on chain-of-thought prompting with at least 5000 citations from before 2020: year + citations
Answer:

8. Find papers on time-traveling cars in Klingon: no good match
Answer:

9. Find me something good about AI: ambiguous
Answer:

10. Recommend a paper: ambiguous
Answer:

## Findings

