def format_history(chat_history: list[dict], agent_name: str) -> str:
    lines = ["Conversation History:"]
    for turn in chat_history:
        user_msg = turn.get("user", "").strip()
        agent_msg = turn.get("agent", "").strip()
        if user_msg:
            lines.append(f"User: {user_msg}")
        if agent_msg:
            lines.append(f"{agent_name}: {agent_msg}")
    return "\n".join(lines)