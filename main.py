from agents.agent_memory_retrieve import should_retrieve_memory

# inputString = input("User input:")

# inputString = "Do you remember seeing John at the party last week?"
inputString = "I'm thinking about ordering the steak. What do you think?"

decision = should_retrieve_memory(inputString)

print("Verdict: "+str(decision.retrieve))
print("Model: "+decision.reasoning+"\n")
