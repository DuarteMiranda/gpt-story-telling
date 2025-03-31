from openai import OpenAI
from pydantic import BaseModel

modelName = "gpt-4o-mini"

def extract_keywords(user_input: str, valid_tags: list[str]) -> list[str]:  
    client = OpenAI()
    prompt = KEYWORD_PROMPT.format(valid_tags=", ".join(valid_tags))
    

    completion = client.beta.chat.completions.parse(
        model=modelName,
        messages=[
        {"role": "system", "content": prompt},  # agent instructions
        {"role": "user", "content": user_input}         # actual message to analyze
    ],
        response_format=RetrieveKeywords,
        temperature=0.2,
    )

    try:
        return completion.choices[0].message.parsed
    except:
        return ["Error generating keywords: "+Exception]  # Fallback if formatting breaks
    
KEYWORD_PROMPT = """
You are an intelligent keyword extraction agent for a dark fantasy world.

You are given a list of approved tags used to classify lore and journal entries. Your job is to extract the most relevant keywords **from this list** based on the user's prompt.

Approved tags: {valid_tags}

Return a Python list of 3–20 relevant tags from the approved list only. Be selective and relevant. Include your reasoning, briefly.
"""

class RetrieveKeywords(BaseModel):
    reasoning: str
    keywords: list[str]