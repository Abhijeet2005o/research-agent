def create_plan(goal: str):
    """
    Break the high-level goal into simple steps.
    Returns a list of steps. Each step is a dictionary.
    """
    # Very simple extraction of the topic from the goal
    topic = goal
    for prefix in ["Research and summarize the top 3 developments in",
                   "Research and summarize",
                   "Summarize the top developments in",
                   "Research"]:
        if goal.lower().startswith(prefix.lower()):
            topic = goal[len(prefix):].strip()
            break

    # Clean the topic a bit
    topic = topic.replace("from the last week", "").replace("last week", "").strip(" .,")

    plan = [
        {
            "id": 1,
            "description": f"Search the web for recent developments about '{topic}'",
            "tool": "web_search"
        },
        {
            "id": 2,
            "description": "Rank the search results and extract important keywords",
            "tool": "analyzer"
        },
        {
            "id": 3,
            "description": "Write a final summary of the top findings",
            "tool": "summarize"
        }
    ]
    return plan