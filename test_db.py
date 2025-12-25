# Test if retrieval works independently of the agent
results = retrieve("What is a ROS 2 node?")
print(f"Found {len(results)} matches in the book.")
for i, text in enumerate(results):
    print(f"{i+1}: {text[:100]}...")