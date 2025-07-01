import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from src.memories.memory import Memory
from src.prompts.prompt import Prompt

load_dotenv()

async def main():
    client = MultiServerMCPClient(
       connections=
       {
            # "math": {
            #     "command": "python",
            #     "args": ["./src/servers/mathserver.py"], # Ensure this is the correct path to your math_server.py file
            #     "transport": "stdio",
            # },
            # "weather": {
            #     "url": "http://localhost:8000/mcp",
            #     "transport": "streamable_http",
            # },
            "azure": {
                "command": "npx",
                "args": ["-y", "@azure/mcp@latest", "server", "start"],
                "env": None,
                "transport": "stdio"
            }
       } 
    )
    
    # Get the tools available from the MCP client
    tools = await client.get_tools()
    
    # Initialize the memory with user and thread IDs
    # Replace "1000" and "5000" with actual user and thread IDs as needed
    memory = Memory("1000", "5000")
    memory.init_az_memory()
    az_memories = memory.get_az_memories()
    
    # Get the system prompt with the Azure memories
    system_prompt = Prompt().get_system_prompt(az_memories)
    
    print(f"System Prompt: {system_prompt}")
    
    # Build the system message with the available tools and memories
    system_message = SystemMessage(content=f"{system_prompt}")
    
    # Initialize the chat model
    # Ensure you have the correct model name and configuration for your Azure OpenAI instance
    llm = init_chat_model("azure_openai:gpt-4o-mini")
    
    # Create the React agent with the chat model, tools, and system message
    agent = create_react_agent(
        llm,
        tools,
        prompt=system_message,
    )
    
    # Invoke the agent with a user message
    async for chunk in agent.astream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Can you get me the claims which took place on 17th June 2025?"
                }
            ]
        }
    ):
        print(chunk)
    
if __name__ == "__main__":
    asyncio.run(main())