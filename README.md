# Research Agent

A small autonomous agent that takes a research goal, plans the steps, uses two tools, handles failures, and produces a summary.

## What it does

1. Accepts a natural language goal
2. Creates a visible plan
3. Uses two tools:
   - Web search (DuckDuckGo)
   - Analyzer (ranks results + extracts keywords)
4. Self-corrects if the search fails (retries with a broader query)
5. Produces a final summary and saves a report

## How to run

```bash
pip install -r requirements.txt

# Normal run
python main.py "Research and summarize the top 3 developments in AI agents from the last week"

# Show self-correction
python main.py "Research and summarize the top 3 developments in renewable energy from the last week" --induce-failure

# Save report
python main.py "Research and summarize the top 3 developments in AI agents from the last week" --out transcripts/run1.md