import os
import jwt 

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.memories.memory import Memory
from src.prompts.prompt import Prompt
from typing import List
from src.states.chat_state_v2 import Message
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()

class Client:
    async def main(self, user_id: str, messages: List[Message]) -> dict:
        """
        Main function to handle the client operations.
        
        Args:
            user_id (str): The ID of the user. user_id = client_id in Cosmos DB.
            messages (List[Message]): List of messages in the chat. messages = messages in Cosmos DB.
            
        Returns:
            str: The response from the agent after processing the messages.
        """
        
        client = MultiServerMCPClient(
            connections=
            {
                "azure": {
                    "command": "npx",
                    "args": ["-y", "@azure/mcp@latest", "server", "start"],
                    "env": None,
                    "transport": "stdio"
                }
            }
        )

        # Get the tools available from the MCP client
        try:
            tools = await client.get_tools()
            print(f"Loaded {len(tools)} tools")
        except Exception as e:
            print(f"Error: {e}")
            return
        
        # Initialize the memory with user and thread IDs
        memory = Memory(user_Id=user_id)
        memory.init_az_memory()
        memory.init_user_memory(user_question=messages[-1]["content"][0]["text"])
        az_memories = memory.get_memories()
        
        # Get the system prompt with the Azure memories
        system_prompt = Prompt().get_system_prompt(az_memories)
        
        # Build the system message with the available tools and memories
        system_message = SystemMessage(content=f"{system_prompt}")
        
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
        
        # Initialize the chat model
        llm = init_chat_model(
            "azure_openai:gpt-4o-mini",
            model_provider = "azure_openai",
            openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
            
            # Azure-specific keyword arguments
            # azure_ad_token_provider = token_provider,
            # azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
        
        # Prepare the chat history from the chat messages & Convert messages to a list of HumanMessage and AIMessage
        history = []
        for turn in messages:
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
        
        # Stream the agent's response message content
        async for chunk in agent.astream(input={"messages": history}):
            print(chunk)
            
        # Invoke the agent with a user message
        response = await agent.ainvoke(
            input = {"messages": history},
        )
        
        return {
            "response": response["messages"][-1].content,
            "tokens_used": response["messages"][-1].response_metadata["token_usage"]["total_tokens"]
        }
        
    def az_details_backup():
        credential = DefaultAzureCredential()
        
        token = credential.get_token("https://cognitiveservices.azure.com/.default")
        print("Access Token:", token.token)
        
        # Decode the JWT token to inspect claims (including tenant info)
        decoded = jwt.decode(token.token, options={"verify_signature": False})
        print("Decoded Token Claims:", decoded)
        print("Tenant ID:", decoded.get("tid"))
        print("Token Provider:", type(credential).__name__)