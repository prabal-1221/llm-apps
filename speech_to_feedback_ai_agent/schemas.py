from typing import TypedDict


class AgentState(TypedDict):
    questions: list[str]
    idx: int = 0
    answers: list[str]
    final_feedback: str
