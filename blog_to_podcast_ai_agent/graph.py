from langgraph.graph import END, START, StateGraph
from nodes import (
    check_contents,
    check_script,
    fetch_blog_content_node,
    generate_conversation_script_node,
    generate_podcast_audio_node,
)
from schemas import AgentState


def build_graph():
    """Initializes and compiles the StateGraph."""
    graph = StateGraph(AgentState)

    # Add Nodes
    graph.add_node("get_contents", fetch_blog_content_node)
    graph.add_node("get_script", generate_conversation_script_node)
    graph.add_node("get_podcast", generate_podcast_audio_node)

    # Add Edges
    graph.add_edge(START, "get_contents")

    graph.add_conditional_edges(
        "get_contents",
        check_contents,
        {True: "get_script", False: END}
    )

    graph.add_conditional_edges(
        "get_script",
        check_script,
        {True: "get_podcast", False: END}
    )

    graph.add_edge("get_podcast", END)

    return graph.compile()
