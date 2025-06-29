import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

async def main():
    client = MultiServerMCPClient(
       connections=
       {  # type: ignore
            "math": {
                "command": "python",
                "args": ["mathserver.py"], # Ensure this is the correct path to your math_server.py file
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
       } 
    )
    
    tools = await client.get_tools()
    
    llm = init_chat_model("azure_openai:gpt-4o-mini")
    
    agent = create_react_agent(
        llm,
        tools,
        prompt="You are a helpful assistant that can use the following tools: {tools}",
    )
    
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather in Tokyo? and what is 10 + 10?"
                }
            ]
        }
    )
    
    print(result['messages'][-1].content)
    
if __name__ == "__main__":
    asyncio.run(main())