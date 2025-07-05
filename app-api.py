import uuid
import uvicorn

from src.states.chat_state_v2 import ChatStateV2
from src.clients.client import Client
from datetime import datetime, timezone
from src.services.cosmos_service.chat_repository import ChatRepository
from fastapi import FastAPI
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend's URL and port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/XChatBot/InitChat/{client_id}/{product_id}")
async def init_chat(client_id: str, product_id: str):
    utc_now = datetime.now(timezone.utc).isoformat()

    chat_state = ChatStateV2(
        id=str(uuid.uuid4()),
        client_id=client_id,
        product_id=product_id,
        role="na",
        messages=[],
        createdAt=utc_now,
        updatedAt=utc_now
    )

    chat_state["messages"].append({
        "role": "system",
        "content": [{
            "type": "text",
            "text": "You are a helpful assistant.",
            "tokensUsed": 0
        }]
    })

    # Initialize chat in Cosmos DB
    init_chat_response = ChatRepository().init_chat(
        chat_state=chat_state
    )

    return init_chat_response

@app.post("/api/XChatBot/ChatCompletion")
async def chat_completion(
    body: dict = Body(...)
):
    chat_id = body.get("chatId")
    client_id = body.get("clientId")
    product_id = body.get("productId")
    message = body.get("message")
    
    # Fetch chat state from Cosmos DB
    chat_state = ChatRepository().get_chat(id=chat_id, client_id=client_id, product_id=product_id)
    
    if not chat_state:
        return {"error": "Chat not found."}

    # Append user message
    chat_state["messages"].append({
        "role": "user",
        "content": [{
            "type": "text",
            "text": message,
            "tokensUsed": 0
        }]
    })

    client = Client()
    
    result = await client.main(
        user_id=client_id,
        messages=chat_state["messages"]
    )

    # Append assistant message
    chat_state["messages"].append({
        "role": "assistant",
        "content": [{
            "type": "text",
            "text": result["response"],
            "tokensUsed": result["tokens_used"]
        }]
    })

    # Update chat in Cosmos DB
    ChatRepository().update_chat(chat_state=chat_state)

    return {
        "messageContent": result["response"],
        "chatId": chat_state["id"],
    }

if __name__ == "__main__":
    uvicorn.run("app-api:app", host="0.0.0.0", port=8000, reload=True)