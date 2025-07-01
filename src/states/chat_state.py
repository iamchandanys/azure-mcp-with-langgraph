from typing import TypedDict, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender, e.g., 'user', 'assistant'")
    message: str = Field(..., description="Content of the message")
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.now(datetime.timezone.utc).isoformat(), description="Timestamp of the message, if available")

class ChatState(TypedDict):
    messages: List[ChatMessage]
    user_id: Optional[str]