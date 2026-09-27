from agent.tools.web_search import web_search
from agent.tools.analyzer import rank_results, top_keywords

def run_plan(goal: str, plan: list, induce_failure: bool = False):
    """
    Execute the plan step by step.
    Returns a dictionary with everything that happened.
    """
    results = {
        "goal": goal,
        "plan": plan,
        "tool_calls": [],
        "ranked_results": [],
        "keywords": [],
        "limitations": [],
        "final_summary": ""
    }

    search_results = []
    failure_already_done = False

    for step in plan:
        step_id = step["id"]
        tool = step["tool"]
        description = step["description"]

        print(f"\n→ Step {step_id}: {description}")

        if tool == "web_search":
            # Simple query from the goal
            query = goal.replace("Research and summarize the top 3 developments in", "")
            query = query.replace("from the last week", "").strip()

            # Deliberate failure for demo
            if induce_failure and not failure_already_done:
                print("  [!] Induced failure for demonstration")
                results["tool_calls"].append({
                    "step": step_id,
                    "tool": "web_search",
                    "input": query,
                    "success": False,
                    "note": "Simulated failure"
                })
                results["limitations"].append(
                    f"Initial search failed (induced). Retrying with broader query..."
                )
                failure_already_done = True

                # Self-correction: broaden the query and try again
                broader_query = query + " overview"
                print(f"  → Retrying with: {broader_query}")
                search_results = web_search(broader_query)
                success = len(search_results) > 0 and "error" not in search_results[0]
                results["tool_calls"].append({
                    "step": step_id,
                    "tool": "web_search",
                    "input": broader_query,
                    "success": success,
                    "note": "self-correction retry"
                })
                if not success:
                    results["limitations"].append("Retry also failed.")
            else:
                # Normal search
                search_results = web_search(query)
                success = len(search_results) > 0 and "error" not in search_results[0]
                results["tool_calls"].append({
                    "step": step_id,
                    "tool": "web_search",
                    "input": query,
                    "success": success
                })
                if not success:
                    results["limitations"].append("Search returned no useful results.")

            print(f"  Got {len(search_results)} results")

        elif tool == "analyzer":
            ranked = rank_results(goal, search_results)
            keywords = top_keywords(search_results)
            results["ranked_results"] = ranked
            results["keywords"] = keywords
            results["tool_calls"].append({
                "step": step_id,
                "tool": "analyzer",
                "input": f"{len(search_results)} results",
                "success": True
            })
            print(f"  Ranked {len(ranked)} results")
            print(f"  Top keywords: {', '.join(keywords[:5])}")

        elif tool == "summarize":
            ranked = results.get("ranked_results", [])
            keywords = results.get("keywords", [])

            # Simple extractive summary (no LLM needed)
            summary_lines = [f"Summary for: {goal}", ""]

            if not ranked:
                summary_lines.append("No useful sources were found.")
            else:
                summary_lines.append("Top findings:")
                for i, r in enumerate(ranked[:3], 1):
                    title = r.get("title", "No title")
                    snippet = r.get("snippet", "")[:180]
                    url = r.get("url", "")
                    summary_lines.append(f"{i}. {title}")
                    summary_lines.append(f"   {snippet}...")
                    summary_lines.append(f"   Source: {url}")
                    summary_lines.append("")

                if keywords:
                    summary_lines.append(f"Key terms: {', '.join(keywords[:6])}")

            results["final_summary"] = "\n".join(summary_lines)
            results["tool_calls"].append({
                "step": step_id,
                "tool": "summarize",
                "input": f"{len(ranked)} ranked results",
                "success": True
            })
            print("  Summary created")

    return results