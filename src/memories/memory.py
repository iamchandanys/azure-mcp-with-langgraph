import os
import uuid

from langchain.embeddings import init_embeddings
from langgraph.store.memory import InMemoryStore
from dotenv import load_dotenv

load_dotenv()

class Memory:
    def __init__(self, user_Id: str):
        self.user_Id = user_Id
        self.memory_namespace = ("memories", user_Id)
        
    def init_az_memory(self):
        """
        Initialize Azure memories.
        """
        
        # Create store
        store = InMemoryStore()
        
        # Store the Azure details in the store
        store.put(self.memory_namespace, str(uuid.uuid4()), {"text": f"Azure subscription ID: {os.getenv("AZ_SUBSCRIPTION_ID")}"})
        store.put(self.memory_namespace, str(uuid.uuid4()), {"text": f"Azure COSMOS DB account name: {os.getenv("AZ_COSMOS_DB_ACCOUNT_NAME")}"})
        store.put(self.memory_namespace, str(uuid.uuid4()), {"text": f"Azure COSMOS DB Database name: {os.getenv("AZ_COSMOS_DB_DATABASE_NAME")}"})
        store.put(self.memory_namespace, str(uuid.uuid4()), {"text": f"Azure COSMOS DB users Container name: {os.getenv("AZ_COSMOS_DB_USERS_CONTAINER_NAME")}"})

        # Retrieve all memories
        memories = store.search(self.memory_namespace)
        
        # Join all values in the dictionary to a string
        memories_str = "\n".join(str(v.value["text"]) for v in memories)
        
        # Store the Azure memories in an instance variable
        # This allows retrieval later without needing to re-fetch from the store
        self.az_memories = memories_str
    
    def init_user_memory(self, user_question: str):
        """
        Initialize user-specific memory.
        """
        
        # Create store with semantic search enabled
        embeddings = init_embeddings(
            "azure_openai:text-embedding-ada-002", 
            openai_api_key=os.getenv("AZURE_TEXT_EMBEDDING_ADA_002_KEY")
        )
        
        # Create store
        store = InMemoryStore(
            index={
                "embed": embeddings,
                "dims": 1536,
            }
        )
        
        # Store user-specific details in the store
        store.put(self.memory_namespace, str(uuid.uuid4()), {"text": f"User ID: {self.user_Id}"})
        store.put(self.memory_namespace, str(uuid.uuid4()), {"text": f"User name is Chandan Y S"})
        store.put(self.memory_namespace, str(uuid.uuid4()), {"text": f"User email is iamchandanys@gmail.com"})
        
        # To search for memories. This will use semantic search
        # and return the most relevant memory based on the query.
        memories = store.search(
            self.memory_namespace, query=user_question, limit=5
        )
        
        # Join all values in the dictionary to a string
        # May add only the highest scoring memory if required
        # More Info: https://github.com/iamchandanys/ds-ml-dl-nlp-learning/blob/main/langgraph/1-basic-chatbot/memory.ipynb
        memories_str = "\n".join(str(v.value["text"]) for v in memories)
        
        self.user_memories = memories_str
    
    def get_memories(self):
        """
        Get all memories.
        """
        
        return self.az_memories + "\n" + self.user_memories
        
# Example usage
if __name__ == "__main__":
    memory = Memory("123")
    memory.init_az_memory()
    memory.init_user_memory("What is my name?")
    print(memory.get_memories())