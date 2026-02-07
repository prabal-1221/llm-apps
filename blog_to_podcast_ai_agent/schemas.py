from typing import TypedDict

from pydantic import BaseModel, Field


# --- Pydantic Models for LLM Output ---
class DialogueLine(BaseModel):
    speaker: str = Field(description="Either 'Host' or 'Guest'")
    message: str = Field(description="The dialogue text")

class ConversationScript(BaseModel):
    conversation: list[DialogueLine]

# --- LangGraph State ---
class AgentState(TypedDict):
    url: str
    content: str | None
    flg_content: bool
    script: ConversationScript | None
    flg_script: bool
