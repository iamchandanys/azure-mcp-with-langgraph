from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.memories.memory import Memory
from src.prompts.prompt import Prompt
from src.states.chat_state import ChatMessage
from typing import List

load_dotenv()

class Client:
    async def main(self, user_id: str, thread_id: str, chat_messages: List[ChatMessage]) -> str:
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
        memory = Memory(user_Id=user_id, thread_Id=thread_id)
        memory.init_az_memory()
        az_memories = memory.get_az_memories()
        
        # Get the system prompt with the Azure memories
        system_prompt = Prompt().get_system_prompt(az_memories)
        
        # Build the system message with the available tools and memories
        system_message = SystemMessage(content=f"{system_prompt}")
        
        # Initialize the chat model
        llm = init_chat_model("azure_openai:gpt-4o-mini")
        
        # Prepare the chat history from the chat messages
        # Convert chat_messages to a list of HumanMessage and AIMessage
        history = []
        for turn in chat_messages:
            if turn["role"] == "user":
                history.append(HumanMessage(content = turn["content"][0]["text"]))
            elif turn["role"] == "assistant":
                history.append(AIMessage(content = turn["content"][0]["text"]))
                
        # Create the React agent with the chat model, tools, and system message
        agent = create_react_agent(
            llm,
            tools,
            prompt=system_message,
        )
        
        # Invoke the agent with a user message
        response = await agent.ainvoke(
            input = {"messages": history},
        )
        
        return response["messages"][-1].content
        
        