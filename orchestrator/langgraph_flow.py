from langgraph.graph import StateGraph, END

from orchestrator.state import AgentState

from llm.extractor import extract_slots

from orchestrator.bank_questions import QUESTIONS


# =========================
# NODE 1 — EXTRACT DATA
# =========================

def extract_node(state: AgentState):

    transcript = state["transcript"]

    extracted = extract_slots(transcript)

    state["extracted_data"].update(extracted)

    return state


# =========================
# NODE 2 — VALIDATE
# =========================

def validate_node(state: AgentState):

    extracted = state["extracted_data"]

    if len(extracted) == 0:

        state["next_action"] = "retry"

    else:

        state["next_action"] = "next_question"

    return state


# =========================
# NODE 3 — RETRY
# =========================

def retry_node(state: AgentState):

    state["retry_count"] += 1

    return state


# =========================
# NODE 4 — NEXT QUESTION
# =========================

def next_question_node(state: AgentState):

    state["current_question"] += 1

    return state


# =========================
# ROUTER
# =========================

def router(state: AgentState):

    if state["next_action"] == "retry":

        return "retry"

    return "next_question"


# =========================
# BUILD GRAPH
# =========================

graph = StateGraph(AgentState)

graph.add_node("extract", extract_node)

graph.add_node("validate", validate_node)

graph.add_node("retry", retry_node)

graph.add_node("next_question", next_question_node)

graph.set_entry_point("extract")

graph.add_edge("extract", "validate")

graph.add_conditional_edges(
    "validate",
    router,
    {
        "retry": "retry",
        "next_question": "next_question"
    }
)

graph.add_edge("retry", END)

graph.add_edge("next_question", END)

workflow = graph.compile()