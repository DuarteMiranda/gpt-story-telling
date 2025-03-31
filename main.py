import os

from agents.agent_memory_retrieve import should_retrieve_memory
from agents.agent_keyword_extractor import extract_keywords
from agents.agent_rolepay import roleplay_agent
from agents.agent_narrative_force import narrative_forcing_agent


from agents.personalities import EVELYNE_PERSONALITY
from agents.personalities import ELEANOR_PERSONALITY
from agents.personalities import KIANA_PERSONALITY

from functions.load_tags import load_lore_entries
from functions.score_lore_entries import score_lore_entries

INCLUDE_AGENT_REASONING = False

lore_data, tag_list = load_lore_entries()

agent_name = "Eleanor"
agent_name_2 = "Kiana"
personality = ELEANOR_PERSONALITY
chat_history = []

START_PROMPT="""You arrive home late at night. As you turn on the light, you're startled to see a pale woman with red eyes smirking in your living room. She slowly walks towards you.
As she passes by a small table, her hand casually brushes against a vase, sending it crashing to the floor. She shrugs her shoulders nonchalantly, bringing her hand up to cover her mouth. Oops. she says in a mock-innocent voice.
Before you can even react, Eleanor moves with blinding speed, pinning you against the wall in the blink of an eye. Her body presses firmly against yours, her strength evident in every muscle.
Leaning in close, she inhales deeply, taking in your scent. She exhales softly and whispers Mmm... you smell better than they usually do."""

chat_history.append({
        "agent": START_PROMPT.strip()
    })

narrative_history= []

retrieve_memory = False

os.system('cls' if os.name == 'nt' else 'clear')

print(f"🩸"+START_PROMPT+"\n")

i=0
added_context=""
added_action=""

while True:
    user_input = input("💬 You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting conversation.")
        break

    added_context=""
    if (retrieve_memory):
        decision = should_retrieve_memory(user_input)

        print("\t⚙️  Verdict: "+str(decision.retrieve))
        print("\t⚙️  Model: "+decision.reasoning+"\n")

        if (decision.retrieve):
            extraction = extract_keywords(user_input,tag_list)

            print("\t⚙️  Keyword reasoning: "+str(extraction.reasoning))
            print("\t⚙️  Model: "+", ".join(extraction.keywords)+"\n")

            ranked_lore = score_lore_entries(lore_data, extraction.keywords)

            for entry in ranked_lore[:3]:
                print(f"\t⚙️  {entry['title']} — score: {entry['score']}")
            
            added_context=ranked_lore[0]["content"]

    added_action=""
    if (len(narrative_history)>2000):
        decision = narrative_forcing_agent(narrative_history,agent_name,user_input,personality)

        print("\t⚙️  Verdict: "+str(decision.reasoning))
        print("\t⚙️  Model: "+decision.action+"\n")

        if (decision.action !="NO CHANGE"):
            added_action=decision.action

        narrative_history.clear()

    if(i%2==0):
        added_action="Add a character action that moves the story forward, after your dialogue"
        print("\t⚙️  Forcing action")

    # Call the agent
    agent_response = roleplay_agent(
        user_input=user_input,
        personality=personality,
        chat_history=chat_history,
        agent_name=agent_name,
        added_context=added_context,
        added_action=added_action
    )

    # Print the agent's reply
    print(f"\n🩸 {agent_name}: {agent_response.agent_reply}\n")
    if(INCLUDE_AGENT_REASONING):
        print(f"🧠 (Reasoning) {agent_name}: {agent_response.reasoning}\n")

    # Update conversation history
    chat_history.append({
        "user": user_input.strip(),
        "agent": agent_response.agent_reply.strip()
    })

    # Update the short time conversation history
    narrative_history.append({
        "user": user_input.strip(),
        "agent": agent_response.agent_reply.strip()
    })

    i=i+1