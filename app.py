import asyncio
import uuid

from src.states.chat_state import ChatState
from src.clients.client import Client

class Chatbot:
    def __init__(self, user_id: str):
        self.chat_state = ChatState(messages = [], user_id = user_id)
        self.client = Client()
        
    async def chat(self):
        while True:
            user_message = input("You: ")
        
            if user_message.lower() == "exit":
                print("========== Chat ended ==========")
                break
            
            self.chat_state["messages"].append({
                "role": "user",
                "message": user_message,
            })
            
            respose = await self.client.main(
                user_id = self.chat_state["user_id"],
                thread_id = str(uuid.uuid4()),
                chat_messages = self.chat_state["messages"]
            )
            
            print(f"Assistant: {respose}")
            
            self.chat_state["messages"].append({
                "role": "assistant",
                "message": respose,
            })
            
if __name__ == "__main__":
    user_id = input("Enter your user ID: ")
    chatbot = Chatbot(user_id)
    
    asyncio.run(chatbot.chat())