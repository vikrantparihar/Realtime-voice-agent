from typing import TypedDict, Dict, List

class AgentState(TypedDict):

    transcript: str

    extracted_data: Dict

    current_question: int

    conversation_history: List[str]

    retry_count: int

    next_action: str