import asyncio
import uuid

from src.states.chat_state_v2 import ChatStateV2
from src.clients.client import Client
from datetime import datetime, timezone
from src.services.cosmos_service.chat_repository import ChatRepository

class Chatbot:
    def __init__(self):
        utc_now = datetime.now(timezone.utc).isoformat()
        
        self.chat_state = ChatStateV2(
            id=str(uuid.uuid4()),
            client_id="81b2e936-9139-4324-b39a-dbf299752365", # Todo: Later store this in emc.b2b.api
            product_id="e03a6aaf-b9e6-4a9e-bd1b-5d56df2949ff", # Todo: Later store this in emc.b2b.api
            role="user",
            messages=[],
            createdAt=utc_now,
            updatedAt=utc_now
        )
        
        self.chat_state["messages"].append({
            "role": "system",
            "content": [{
                "type": "text",
                "text": "You are a helpful assistant.",
                "tokensUsed": 0
            }]
        })
        
        self.client = Client()
        
    async def chat(self):
        while True:
            user_message = input("You: ")
        
            if user_message.lower() == "exit":
                print("========== Chat ended ==========")
                break
            
            self.chat_state["messages"].append({
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": user_message,
                    "tokensUsed": 0
                }]
            })
            
            respose = await self.client.main(
                user_id = self.chat_state["client_id"],
                messages = self.chat_state["messages"]
            )
            
            print(f"Assistant: {respose}")
            
            self.chat_state["messages"].append({
                "role": "assistant",
                "content": [{
                    "type": "text",
                    "text": respose,
                    "tokensUsed": 0 # Todo: Assign the actual tokens used
                }]
            })
            
if __name__ == "__main__":
    chatbot = Chatbot()
    asyncio.run(chatbot.chat())