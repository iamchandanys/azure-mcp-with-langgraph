# async for event in agent.astream(
#     {
#       "messages": history
#     }
# ):
#     for value in event.values():
#         print(value["messages"])  # Print the last message content from each event


# "math": {
#     "command": "python",
#     "args": ["./src/servers/mathserver.py"], # Ensure this is the correct path to your math_server.py file
#     "transport": "stdio",
# },
# "weather": {
#     "url": "http://localhost:8000/mcp",
#     "transport": "streamable_http",
# },