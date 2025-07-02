import asyncio
import uuid

from src.states.chat_state_v2 import ChatStateV2
from src.clients.client import Client
from datetime import datetime, timezone

class Chatbot:
    def __init__(self, user_id: str):
        utc_now = datetime.now(timezone.utc).isoformat()
        
        self.chat_state = ChatStateV2(
            id=str(uuid.uuid4()),
            client_id=user_id,
            product_id="mcp-with-langgraph",
            role="user",
            messages=[],
            createdAt=utc_now,
            updatedAt=utc_now
        )
        
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
                thread_id = self.chat_state["id"],
                chat_messages = self.chat_state["messages"]
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
    user_id = input("Enter your user ID: ")
    chatbot = Chatbot(user_id)
    asyncio.run(chatbot.chat())