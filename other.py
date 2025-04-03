"""

main_loop = False
while main_loop:
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

    i=i+1"
"
"""