from typing import TypedDict


class Agentstate(TypedDict):
    questions: list[str]
    idx: int = 0
    is_questions_empty: bool = True
    answers: list[str]
    final_feedback: str
