from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
modelName = "gpt-4o-mini"

def should_retrieve_memory(user_input):
    client = OpenAI()

    completion = client.beta.chat.completions.parse(
        model=modelName,
        messages=[
        {"role": "system", "content": THOUGHT_PROMPT},  # agent instructions
        {"role": "user", "content": user_input}         # actual message to analyze
    ],
        response_format=RetrieveEvent,
        temperature=0.2,
    )

    decision = completion.choices[0].message.parsed
    return decision

THOUGHT_PROMPT = """
You are an intelligent storytelling agent that simulates thought before responding.

Your job is to decide whether the user's message requires retrieving long-term memory (such as lore, character backstory, or past events) or if it can be answered with recent short-term memory alone.

Consider:
1. Does the message mention any specific people, places, events, or time references?
2. Is the information likely to be outside the current conversation?
3. Would retrieving background context improve the response?

Think internally before answering. Your final output should be either True or False.
"""

class RetrieveEvent(BaseModel):
    reasoning: str
    retrieve: bool