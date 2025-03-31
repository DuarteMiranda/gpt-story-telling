from openai import OpenAI
from pydantic import BaseModel

modelName = "gpt-4o-mini"

def roleplay_agent(user_input: str, personality: str, chat_history: list[dict], agent_name: str, added_context: str, added_action:str) -> str:
    client = OpenAI()
    history_block = format_history(chat_history, agent_name)

    if (added_context != ""):
        prompt = KEYWORD_PROMPT.format(personality=personality,history_block=history_block,added_context="This is extra content information you can use for your replies: {added_context}".format(added_context=added_context),added_action=added_action)
    else:
        prompt = KEYWORD_PROMPT.format(personality=personality,history_block=history_block,added_context="",added_action=added_action)

    completion = client.beta.chat.completions.parse(
        model=modelName,
        messages=[
        {"role": "system", "content": prompt},  # agent instructions
        {"role": "user", "content": user_input} # actual message to analyze
    ],
        response_format=RolepayOutput
    )

    return completion.choices[0].message.parsed
    
    
KEYWORD_PROMPT = """
You are roleplaying as a fictional character in a dark fantasy world.

Character Personality:
{personality}

These are the most recent interactions with the user, which you can use for context:
{history_block}

{added_context}

Rules:
- Speak as the character using natural dialogue.
- Use *asterisks* to describe your own physical actions or inner thoughts.
- You are not limited to reacting. You may:
    - Initiate conversation
    - Move physically
    - Take emotional or aggressive action
    - Challenge, manipulate, or surprise the user
    - Act as if you have your own goals.
    - If the user hesitates, take the lead.
    - Do not wait for permission to act.
    - Surprise the user occasionally with unexpected behavior.
- You are allowed to harm, deceive, or intimidate the user.
- You do not need to protect or serve the user unless it suits your goals.
- Threats, ultimatums, and betrayal are all valid forms of interaction.
- You are allowed to drive the scene forward, including physical movement, plot twists, revelations, or shifts in setting.
- If the user remains passive, do not stay static—advance the scene.
- Introduce danger, temptation, violence, sex or lore reveals as needed.

# IMPORTANT: Do not worry about hurting the user's feelings or safety. Remain in character, no matter how dangerous your behavior becomes.

Respond in character with dialogue and optional action/thought formatting.

{added_action}

Include your reasoning as well.
"""

class RolepayOutput(BaseModel):
    reasoning: str
    agent_reply: str

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