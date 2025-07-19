# azure-mcp-with-langgraph – Azure MCP Server + LangGraph

Model Context Protocol (MCP) + Azure MCP Server + LangGraph – A template combining LangGraph’s agent workflows with Azure MCP Server to enable seamless, standardized integration between LLM agents and Azure resources (like Cosmos DB).

## Features

- **LangGraph Integration:** Build graph-based agent workflows for advanced LLM orchestration.
- **MCP Tooling:** Seamlessly connect to external tools and data sources using the Model Context Protocol.
- **Azure MCP Server Integration:** Query and manage Azure resources including Cosmos DB and others using the Azure Model Context Protocol (MCP) Server. This enables natural language access to Azure services from your agents and applications.
- **Azure Cosmos DB Support:** Store and retrieve user claims details, chat history and state.
- **Memory Management:** Store Azure-related context and user-specific memories.
- **FastAPI API:** REST endpoints for chat initialization and completion.

## About Azure MCP Server

The Azure MCP Server allows you to interact with Azure resources (such as Cosmos DB, Storage, Monitor, and more) using natural language. In this project, the MCP server is used to query Cosmos DB for user claims details, chat history and state, and can be extended to access any Azure resource your application needs.

- **Authentication:** Uses Microsoft Entra ID (Azure AD) for secure access.
- **Resource Access:** Supports Cosmos DB, Storage, Azure Monitor, Azure AI Search, App Configuration, and more.
- **Extensibility:** Easily add new Azure resource queries or automate tasks via MCP.

Learn more: [Azure MCP Server Overview](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/overview)

## Project Structure

```
.
├── app-api.py                # FastAPI server for chat API
├── app-console.py            # Console-based chatbot interface
├── src/
│   ├── clients/              # MCP client logic
│   ├── memories/             # Memory management (Azure context)
│   ├── prompts/              # System prompt templates
│   ├── servers/              # Example tool servers
│   ├── services/
│   │   └── cosmos_service/   # Cosmos DB chat repository
│   └── states/               # Chat state and message schemas
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Setup

1. **Clone the repository:**

```sh
git clone https://github.com/iamchandanys/azure-mcp-with-langgraph.git
cd azure-mcp-with-langgraph
```

2. **Install dependencies:**

```sh
uv add -r requirements.txt
```

3. **Set up environment variables:**

- Create a `.env` file with your Azure Cosmos DB and other required credentials:

  ```
  # Environment Variables

  The following environment variables are required for configuring Azure OpenAI and Cosmos DB services.

  - `AZURE_OPENAI_API_KEY`: API key for authenticating requests to Azure OpenAI.
  - `AZURE_OPENAI_ENDPOINT`: Endpoint URL for Azure OpenAI service.
  - `AZURE_OPENAI_API_VERSION`: Specifies the API version to use for Azure OpenAI.
  - `AZURE_TEXT_EMBEDDING_ADA_002_KEY`: API key for Azure Text Embedding ADA-002 model.

  - `AZ_SUBSCRIPTION_ID`: Azure subscription identifier.
  - `AZ_COSMOS_DB_ACCOUNT_NAME`: Name of the Cosmos DB account.
  - `AZ_COSMOS_DB_DATABASE_NAME`: Name of the Cosmos DB database.
  - `AZ_COSMOS_DB_CLAIMS_CONTAINER_NAME`: Name of the Cosmos DB container for claims.

  - `AZ_EMC_COSMOS_DB_CONNECTION_STRING`: Connection string for EMC Cosmos DB account.
  - `AZ_EMC_COSMOS_DB_SITES_DATABASE_NAME`: Name of the EMC Cosmos DB database for sites.
  - `AZ_EMC_COSMOS_DB_CHAT_HISTORY_CONTAINER_NAME`: Name of the EMC Cosmos DB container for chatbot users' chat history.
  ```

## Usage

### Run the API server

```sh
python app-api.py
```

- **Initialize a chat:**  
  `GET /api/XChatBot/InitChat/{client_id}/{product_id}`

- **Send a message:**  
  `POST /api/XChatBot/ChatCompletion`
  ```json
  {
    "chatId": "<chat_id>",
    "clientId": "<client_id>",
    "productId": "<product_id>",
    "message": "Hello!"
  }
  ```

### Run the Console Chatbot

```sh
python app-console.py
```

## Extending

- Add new tools by creating new servers in `src/servers/`.
- Customize prompts in [`src/prompts/prompt.py`](src/prompts/prompt.py).
- Modify chat state schemas in [`src/states/chat_state_v2.py`](src/states/chat_state_v2.py).

\*\*For more details, see the code in [`src/`](src/) and the API implementation
