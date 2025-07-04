# mcp-with-langgraph

Model Context Protocol (MCP) + LangGraph – A template combining LangGraph’s graph-based agent workflows with MCP to enable seamless, standardized integration between LLM agents and external tools/data sources.

## Features

- **LangGraph Integration:** Build graph-based agent workflows for advanced LLM orchestration.
- **MCP Tooling:** Seamlessly connect to external tools and data sources using the Model Context Protocol.
- **Azure Cosmos DB Support:** Store and retrieve chat history and state.
- **Memory Management:** Store Azure-related context and user-specific memories.
- **Extensible Tool Servers:** Example math and weather servers included.
- **FastAPI API:** REST endpoints for chat initialization and completion.

## Project Structure

```
.
├── app-api.py                # FastAPI server for chat API
├── app-console.py            # Console-based chatbot interface
├── src/
│   ├── clients/              # MCP client logic
│   ├── memories/             # Memory management (Azure context)
│   ├── prompts/              # System prompt templates
│   ├── servers/              # Example tool servers (math, weather)
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
   git clone <repo-url>
   cd mcp-with-langgraph
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file with your Azure Cosmos DB and other required credentials:
     ```
     AZ_EMC_COSMOS_DB_CONNECTION_STRING=...
     AZ_EMC_COSMOS_DB_SITES_DATABASE_NAME=...
     AZ_EMC_COSMOS_DB_CHAT_HISTORY_CONTAINER_NAME=...
     AZ_SUBSCRIPTION_ID=...
     AZ_COSMOS_DB_ACCOUNT_NAME=...
     AZ_COSMOS_DB_DATABASE_NAME=...
     AZ_COSMOS_DB_CLAIMS_CONTAINER_NAME=...
     ```

## Usage

### Run the API server

```sh
uvicorn app-api:app --reload
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

### Example Tool Servers

- Math server:  
  ```sh
  python src/servers/mathserver.py
  ```
- Weather server:  
  ```sh
  python src/servers/weatherserver.py
  ```

## Extending

- Add new tools by creating new servers in `src/servers/`.
- Customize prompts in [`src/prompts/prompt.py`](src/prompts/prompt.py).
- Modify chat state schemas in [`src/states/chat_state_v2.py`](src/states/chat_state_v2.py).

## License

MIT License

---

**For more details, see the code in [`src/`](src/) and the API implementation
