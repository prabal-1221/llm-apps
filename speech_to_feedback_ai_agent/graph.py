from langgraph.graph import END, START, StateGraph
from nodes import run_ask_question, run_intial_configuration, run_record_and_transcribe_answer
from schemas import Agentstate


# TODO: Incomplete Graph
def build_graph():
    workflow = StateGraph(Agentstate)

    workflow.add_node("intial_configuration", run_intial_configuration)
    workflow.add_node("ask_question", run_ask_question)
    workflow.add_node("record_and_transcribe_answer", run_record_and_transcribe_answer)

    workflow.add_edge(START, "intial_configuration")
    workflow.add_edge("intial_configuration", "ask_question")
    workflow.add_edge("ask_question", "record_and_transcribe_answer")
    workflow.add_edge("record_and_transcribe_answer", END)

