from langgraph.graph import END, START, StateGraph
from nodes import (
    run_capture_and_process_response,
    run_check_system_readiness,
    run_decide_next_step,
    run_deliver_question,
    run_initialize_session,
)
from schemas import AgentState


# TODO: Incomplete Graph
def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("initialize_session", run_initialize_session)
    workflow.add_node("deliver_question", run_deliver_question)
    workflow.add_node("capture_and_process_response", run_capture_and_process_response)

    workflow.add_edge(START, "initialize_session")
    workflow.add_conditional_edges(
        "initialize_session",
        run_check_system_readiness,
        {
            "success": "deliver_question",
            "failure": END
        }
    )

    workflow.add_edge("deliver_question", "capture_and_process_response")
    workflow.add_conditional_edges(
        "capture_and_process_response",
        run_decide_next_step,
        {
            "yes": "deliver_question",
            "no": END
        }
    )

    return workflow.compile()

