from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.graph.state import HealthcareState

from app.graph.nodes import (
    analyze_report_node,
    health_agent_node,
    comparison_node,
    recommendation_node,
    final_response_node
)


def build_healthcare_graph():

    builder = StateGraph(
        HealthcareState
    )

    # -------------------------
    # Nodes
    # -------------------------

    builder.add_node(
        "analyze_report",
        analyze_report_node
    )

    builder.add_node(
        "health_agent",
        health_agent_node
    )

    builder.add_node(
        "compare_reports",
        comparison_node
    )

    builder.add_node(
        "recommendation_agent",
        recommendation_node
    )

    builder.add_node(
        "final_response",
        final_response_node
    )

    # -------------------------
    # Edges
    # -------------------------

    builder.add_edge(
        START,
        "analyze_report"
    )

    builder.add_edge(
        "analyze_report",
        "health_agent"
    )

    builder.add_edge(
        "health_agent",
        "compare_reports"
    )

    builder.add_edge(
        "compare_reports",
        "recommendation_agent"
    )

    builder.add_edge(
        "recommendation_agent",
        "final_response"
    )

    builder.add_edge(
        "final_response",
        END
    )

    return builder.compile()


healthcare_graph = build_healthcare_graph()