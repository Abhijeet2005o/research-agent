# Design Write-up

## Goal
Build a small agent that can research a topic by itself: plan, use tools, recover from failure, and report results.

## Design decisions

- Two different tools: one does network search, the other does local ranking. This shows real tool diversity.
- Planning happens first and is printed so the process is visible.
- Self-correction is handled in the executor. If search fails, it broadens the query and tries once more. If it still fails, the agent continues and reports the limitation instead of crashing.
- The summary is extractive (taken from the top ranked results). This keeps the agent simple and free of any paid API key.

## Limitations

- The planner is rule-based, so it works best for “research and summarize” style goals.
- Ranking is based on simple keyword overlap, not deep understanding.
- No LLM is required, which makes the agent easy to run but limits the quality of the final summary.

## What I would improve with more time

- Add a real LLM (local Ollama or free Gemini) for better planning and summarization.
- Make the retry logic smarter.
- Add more tools (for example reading a full page).