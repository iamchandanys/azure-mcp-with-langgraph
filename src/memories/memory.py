import os
import uuid

from langchain.embeddings import init_embeddings
from langgraph.store.memory import InMemoryStore
from dotenv import load_dotenv

load_dotenv()

class Memory:
    def __init__(self, user_Id: str, thread_Id: str):
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
        store.put(self.memory_namespace, str(uuid.uuid4()), {"text": f"Azure COSMOS DB claims Container name: {os.getenv("AZ_COSMOS_DB_CLAIMS_CONTAINER_NAME")}"})
        
        # Retrieve all memories
        memories = store.search(self.memory_namespace)
        
        # Join all values in the dictionary to a string
        memories_str = "\n".join(str(v.value["text"]) for v in memories)
        
        # Store the Azure memories in an instance variable
        # This allows retrieval later without needing to re-fetch from the store
        self.az_memories = memories_str
        
    def get_az_memories(self):
        """
        Retrieve the Azure memories.
        """
        return self.az_memories
        
        
# Example usage
if __name__ == "__main__":
    memory = Memory("123", "456")
    memory.init_az_memory()
    print(memory.get_az_memories())