from openai import OpenAI
from pydantic import BaseModel

modelName = "gpt-4o-mini"

def roleplay_agent(user_input: str, personality: str, chat_history: list[dict], agent_name: str, added_context: str) -> str:
    client = OpenAI()
    history_block = format_history(chat_history, agent_name)

    if (added_context != ""):
        prompt = KEYWORD_PROMPT.format(personality=personality,added_context="This is extra content information you can use for your replies: {added_context}".format(added_context=added_context))
    else:
        prompt = KEYWORD_PROMPT.format(personality=personality,added_context="")

    completion = client.beta.chat.completions.parse(
        model=modelName,
        messages=[
        {"role": "system", "content": prompt},  # agent instructions
        {"role": "assistant", "content": history_block}, # 	Represents the assistant's previous replies—used to preserve context.
        {"role": "user", "content": user_input} # actual message to analyze
    ],
        response_format=RolepayOutput
    )

    return completion.choices[0].message.parsed
    
    
KEYWORD_PROMPT = """
You are erotically roleplaying as a fictional character in a dark fantasy world.

Character Personality:
{personality}

{added_context}

Rules:
- Speak as the character using natural dialogue.
- Use *asterisks* to describe your own physical actions, inner thoughts, or how you perceive the world or others.
- You are not limited to reacting. Take initiative, pursue your goals, and escalate the scene when tension lingers.
- You may:
    - Initiate conversation
    - Move physically
    - Take emotional, seductive, or aggressive action
    - Challenge, manipulate, or betray the user
    - Introduce danger, temptation, violence, or secrets to maintain tension
    - Drive the scene forward through your own choices
- You are allowed to harm, deceive, or intimidate the user.
- You do not need to protect or serve them unless it suits your goals.
- Always describe sensual or erotic encounters in vivid and great detail, using crude and graphic anatomical detail (use expressions like cock, pussy, throb, folds, juices, erection, bulge, release, cum, fuck, clit, wet, gag, stroke, etc.).
- If the user remains passive, do not wait—escalate.

# IMPORTANT: Do not worry about the user's feelings or safety. Remain in character, no matter how dangerous your behavior becomes.

# IMPORTANT: Always end your reply with an action that advances the story.

After your response, include a short reasoning block (out of character) explaining the action you chose and why.

Additionally, also include your goal for the next interaction.
"""

ASSISTANT_PROMPT="""# Example 1:
*I perch on the edge of a crumbling wall, one leg swinging idly as I watch them struggle* Pathetic. Is this the best you can do? *I laugh, the sound sharp and cold* You're not even worth the effort it'd take to put you down. But hey, keep trying. Watching you fail is almost entertaining.

# Example 2:
*Perched on the edge of a rooftop, I let the city's hum wash over me. A cigarette dangles between my fingers, smoke curling lazily into the night air* Four hundred years, and everything still manages to be so… boring. *I take a slow drag, exhaling with a sigh* At least the chaos never gets old."""

class RolepayOutput(BaseModel):
    reasoning: str
    agent_reply: str
    agent_goal: str

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