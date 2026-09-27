import argparse
from agent.planner import create_plan
from agent.executor import run_plan

def save_report(result, filename):
    """Save a clean Markdown report."""
    lines = []
    lines.append(f"# Run Report: {result['goal']}")
    lines.append("")
    lines.append("## Plan (visible planning trace)")
    for step in result["plan"]:
        lines.append(f"{step['id']}. **[{step['tool']}]** {step['description']}")
    lines.append("")
    lines.append("## Tool Call Log")
    for tc in result["tool_calls"]:
        status = "OK" if tc.get("success") else "FAILED"
        note = f" (note: {tc['note']})" if tc.get("note") else ""
        lines.append(f"- [{status}] **{tc['tool']}** — input: `{tc['input']}`{note}")
    lines.append("")
    if result["limitations"]:
        lines.append("## Limitations Encountered")
        for lim in result["limitations"]:
            lines.append(f"- {lim}")
        lines.append("")
    lines.append("## Final Summary")
    lines.append(result.get("final_summary", "No summary produced"))
    lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nReport saved to: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Research Agent")
    parser.add_argument("goal", help="The research goal")
    parser.add_argument("--induce-failure", action="store_true",
                        help="Deliberately fail the first search to show self-correction")
    parser.add_argument("--out", default=None,
                        help="Save report to this filename (example: transcripts/run1.md)")
    args = parser.parse_args()

    goal = args.goal

    print("GOAL:", goal)
    print("\nCreating plan...")
    plan = create_plan(goal)

    print("\nPLAN:")
    for step in plan:
        print(f"  {step['id']}. [{step['tool']}] {step['description']}")

    print("\nExecuting plan...")
    result = run_plan(goal, plan, induce_failure=args.induce_failure)

    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    print(result.get("final_summary", "No summary produced"))

    if result["limitations"]:
        print("\nLimitations:")
        for lim in result["limitations"]:
            print("-", lim)

    if args.out:
        save_report(result, args.out)

if __name__ == "__main__":
    main()