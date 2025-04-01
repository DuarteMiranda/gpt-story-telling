import os

from agents.agent_memory_retrieve import should_retrieve_memory
from agents.agent_keyword_extractor import extract_keywords
from agents.agent_rolepay import roleplay_agent
from agents.agent_narrative_force import narrative_forcing_agent


from agents.personalities import Character
from agents.personalities import CHARACTERS
from functions.load_tags import load_lore_entries
from functions.score_lore_entries import score_lore_entries

INCLUDE_AGENT_REASONING = True

lore_data, tag_list = load_lore_entries()

CHARACTER = CHARACTERS["daughters"]
agent_name = CHARACTER.name
personality = CHARACTER.personality
start_prompt= CHARACTER.starting_prompt

chat_history = []

chat_history.append({
        "agent": start_prompt.strip()
    })

narrative_history= []

retrieve_memory = False

os.system('cls' if os.name == 'nt' else 'clear')

print(f"🩸"+start_prompt+"\n")

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

    # Call the agent
    agent_response = roleplay_agent(
        user_input=user_input,
        personality=personality,
        chat_history=chat_history,
        agent_name=agent_name,
        added_context=added_context
    )

    # Print the agent's reply
    print(f"\n🩸 {agent_name}\n {agent_response.agent_reply}\n")
    if(INCLUDE_AGENT_REASONING):
        print(f"🧠 (Reasoning) {agent_response.reasoning}\n")
        print(f"🧠 (Goal) {agent_response.agent_goal}\n")

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