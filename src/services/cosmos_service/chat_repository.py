import os

from azure.cosmos import CosmosClient, exceptions
from src.states.chat_state_v2 import ChatStateV2

class ChatRepository:
    def __init__(self):
        self.client = CosmosClient.from_connection_string(os.getenv("AZ_EMC_COSMOS_DB_CONNECTION_STRING"))
        self.db = self.client.get_database_client(os.getenv("AZ_EMC_COSMOS_DB_SITES_DATABASE_NAME"))
        self.container = self.db.get_container_client(os.getenv("AZ_EMC_COSMOS_DB_CHAT_HISTORY_CONTAINER_NAME"))
        
    def init_chat(self, chat_state: ChatStateV2) -> ChatStateV2:
        """
        Initialize a new chat in the Cosmos DB.
        :param chat_state: ChatStateV2 object containing chat details.
        :return: The created chat state with its ID.
        """
        
        try:
            response = self.container.create_item(
                body=chat_state,
            )
            return response
        except exceptions.CosmosHttpResponseError as e:
            print(f"An error occurred while creating the chat: {e}")
            return None
        
    def get_chat(self, id: str, client_id: str, product_id: str) -> ChatStateV2:
        """
        Retrieve a chat by its ID from the Cosmos DB.
        :param id: The ID of the chat to retrieve.
        :param client_id: The client ID for the partition key.
        :param product_id: The product ID for the partition key.
        :return: ChatStateV2 object if found, None otherwise.
        """
        
        try:
            response = self.container.read_item(
                item=id,
                partition_key=[client_id, product_id]
            )
            return response
        except exceptions.CosmosResourceNotFoundError:
            print(f"Chat with ID {id} not found.")
            return None
        except exceptions.CosmosHttpResponseError as e:
            print(f"An error occurred while retrieving the chat: {e}")
            return None
        
    def update_chat(self, chat_state: ChatStateV2):
        """
        Update an existing chat in the Cosmos DB.
        :param chat_state: ChatStateV2 object containing updated chat details.
        :return: The updated chat state if successful, None otherwise.
        """
        
        try:
            response = self.container.upsert_item(
                body=chat_state
            )
            return response
        except exceptions.CosmosHttpResponseError as e:
            print(f"An error occurred while updating the chat: {e}")
            return None
