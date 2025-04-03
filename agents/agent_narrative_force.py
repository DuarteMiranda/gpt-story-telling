from openai import OpenAI
from pydantic import BaseModel

modelName = "gpt-4o-mini"

def narrative_forcing_agent(chat_history: list[dict], agent_name: str, user_input: str, personality: str, medium_term_context: str) -> str:
    client = OpenAI()
    history_block = format_history(chat_history, agent_name)

    context_block = f"Medium Term-Context:\n{medium_term_context}" if medium_term_context else ""

    prompt = KEYWORD_PROMPT.format(
        history_block=history_block,
        personality=personality,
        user_input=user_input,
        medium_term_context=context_block
    )
    
    completion = client.beta.chat.completions.parse(
        model=modelName,
        messages=[
        {"role": "system", "content": prompt}
    ],
        response_format=NarrativeOutput
    )

    return completion.choices[0].message.parsed
    
    
KEYWORD_PROMPT = """
You are a narrative escalation agent for a dark fantasy role-play system.

Your job is to detect when the character is stuck in a passive reaction loop and determine if their behavior should escalate to keep the story emotionally engaging.

IMPORTANT:
- You are not allowed to introduce new events, locations, characters, or external forces.
- You may ONLY suggest escalation through the character's own actions.
- Do not invent anything outside the character's established presence in the scene.

Instructions:
Based on the user's last message and the character's response, decide if the character act.
Provide either:
- A single-sentence suggestion describing how the character should escalate next, OR
- 'NO CHANGE' if the scene is already progressing or does not require escalation.

{medium_term_context}

Conversation History:  
{history_block}

Character personality:
{personality}

This was the user's last message:
{user_input}

What should the character do next to avoid narrative stagnation?"""

class NarrativeOutput(BaseModel):
    reasoning: str
    action: str

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