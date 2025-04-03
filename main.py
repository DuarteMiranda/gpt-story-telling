import os
import streamlit as st
import datetime
import tiktoken
import streamlit.components.v1 as components

from agents.agent_memory_retrieve import should_retrieve_memory
from agents.agent_keyword_extractor import extract_keywords
from agents.agent_rolepay import roleplay_agent
from agents.agent_narrative_force import narrative_forcing_agent
from agents.agent_summary import summary_agent

from agents.personalities import Character
from agents.personalities import CHARACTERS
from functions.load_tags import load_lore_entries
from functions.score_lore_entries import score_lore_entries

INCLUDE_AGENT_REASONING = True
INCLUDE_CHAT = False
INCLUDE_SHORTENED_MEMORY = True
SHORT_TERM_MEMORY_LIMIT_TOKENS = 1200

lore_data, tag_list = load_lore_entries()

CHARACTER = CHARACTERS["drKind"]
agent_name = CHARACTER.name
personality = CHARACTER.personality
start_prompt= CHARACTER.starting_prompt

def estimate_token_count(messages, model="gpt-4o-mini"):
    enc = tiktoken.encoding_for_model(model)
    total = 0
    for turn in messages:
        total += len(enc.encode(turn["user"])) + len(enc.encode(turn["agent"]))
    return total

def summarize_history(messages,agent_name, model="gpt-4o-mini"):
    enc = tiktoken.encoding_for_model(model)
    message_to_summarize = ""
    for turn in messages:
        message_to_summarize = message_to_summarize + "\n" + turn["user"] + "\n"+ turn["agent"]
        total = len(enc.encode(message_to_summarize))
        turn["summarized"]=True
        if (total>SHORT_TERM_MEMORY_LIMIT_TOKENS):
            break

    return summary_agent(message_to_summarize)

if "medium_term_memory" not in st.session_state:
    st.session_state.medium_term_memory=""

added_context=""
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "user": "",
        "agent": start_prompt.strip(),
        "summarized": False
    })

with st.sidebar:
    st.markdown("## 🛠 Dev Tools")
    INCLUDE_AGENT_REASONING = st.toggle("Show Agent Reasoning", value=False)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if (str(message["user"])!=""):
        with st.chat_message("user",avatar=":material/face:"):
            st.badge("You",color="violet")
            st.markdown(message["user"])


    with st.chat_message("agent",avatar=":material/face_3:"):
        st.badge(agent_name)
        st.markdown(message["agent"])

# Accept user input
if prompt := st.chat_input("Message"):
    # Display user message in chat message container
    scroll_to_bottom()
    with st.chat_message("user"):
        st.markdown(prompt)

    if(INCLUDE_CHAT): print("💬 You: "+prompt)
   
 # Display assistant response in chat message container
    with st.chat_message("assistant",avatar=":material/face_3:"):
        # Call the agent
        agent_response = roleplay_agent(
            user_input=prompt,
            personality=personality,
            chat_history=[msg for msg in st.session_state.messages if msg.get("summarized") is False],
            agent_name=agent_name,
            added_context=added_context,
            medium_term_context=st.session_state.medium_term_memory
        )
        response = st.markdown(agent_response.agent_reply)

        if(INCLUDE_CHAT): print(f"\n🩸 {agent_name}\n {agent_response.agent_reply}\n")
        if(INCLUDE_AGENT_REASONING):
            print(f"🧠 (Reasoning) {agent_response.reasoning}\n")
            print(f"🎯 (Goal) {agent_response.agent_goal}\n")

        if INCLUDE_AGENT_REASONING:
            st.markdown("---")
            st.markdown(f"**🧠 Reasoning:**\n{agent_response.reasoning}")
            st.markdown(f"**🎯 Goal:**\n{agent_response.agent_goal}")

    # Update conversation history
    st.session_state.messages.append({
        "user": prompt.strip(),
        "agent": agent_response.agent_reply.strip(),
        "reasoning": agent_response.reasoning,
        "agent_goal": agent_response.agent_goal,
        "timestamp": datetime.datetime.now(),
        "summarized": False
    })

    free_messages = [msg for msg in st.session_state.messages if msg.get("summarized") is False]

    token_count = estimate_token_count(messages=free_messages)

    if(INCLUDE_SHORTENED_MEMORY): print(f"\n🧠 Token Count: {token_count}")

    if token_count>SHORT_TERM_MEMORY_LIMIT_TOKENS:
        medium_term_memory = summarize_history(messages=free_messages,agent_name=agent_name)
        st.session_state.medium_term_memory=st.session_state.medium_term_memory+"\n"+medium_term_memory
        if(INCLUDE_SHORTENED_MEMORY):
            print(f"\n🧠 Summarized medium term memory to: {st.session_state.medium_term_memory}")

# Call this at the very end of your page







