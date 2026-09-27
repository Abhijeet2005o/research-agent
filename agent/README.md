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
main.py                 # Entry point
agent/
  planner.py            # Creates the plan
  executor.py           # Runs the plan and handles failures
  tools/
    web_search.py       # Tool 1: live web search
    analyzer.py         # Tool 2: ranking + keywords
docs/
  WRITEUP.md            # Design decisions and limitations
  architecture.txt      # Simple architecture diagram
transcripts/            # Sample run reportspip install -r requirements.txt
transcripts/run1_ai_agents.md — normal successful run
transcripts/run2_failure.md — induced failure + recovery
transcripts/final_normal.md — another normal run
transcripts/final_failure.md — another failure + recovery run

# Normal run
python main.py "Research and summarize the top 3 developments in AI agents from the last week"

# Show self-correction
python main.py "Research and summarize the top 3 developments in renewable energy from the last week" --induce-failure

# Save report
python main.py "Research and summarize the top 3 developments in AI agents from the last week" --out transcripts/run1.md
