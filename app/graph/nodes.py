from app.graph.state import HealthcareState

from app.agents.report_analyzer import (
    analyze_health_report
)

from app.agents.health_agent import (
    run_health_agent
)

from app.agents.recommendation_agent import (
    generate_recommendations
)

from app.tools.comparision_tool import (
    compare_reports
)


def analyze_report_node(
    state: HealthcareState
):

    print("\n" + "=" * 60)
    print("NODE: ANALYZE REPORT")
    print("=" * 60)

    report = state["uploaded_report"]

    result = analyze_health_report(
        report
    )

    print("\nReport analysis completed.")

    print(result.model_dump())

    return {
        "report_analysis": result.model_dump()
    }

def health_agent_node(state: HealthcareState):
    print("\n" + "=" * 60)
    print("NODE: HEALTH AGENT")
    print("=" * 60)

    print("\nPatient ID from state:")
    print(repr(state.get("patient_id")))

    print("\nReport analysis from state:")
    print(state.get("report_analysis"))

    patient_id = state["patient_id"]
    report_analysis = state["report_analysis"]

    documents = run_health_agent(
        patient_id=patient_id,
        report_analysis=report_analysis
    )

    print(f"\nHealth Agent returned: {len(documents)} documents")

    # for i, document in enumerate(documents, 1):
    #     print(f"\n--- Document {i} ---")
    #     print(document["metadata"])

    return {
        "retrieved_documents": documents
    }
def comparison_node(
    state: HealthcareState
):

    print("\n" + "=" * 60)
    print("NODE: COMPARE REPORTS")
    print("=" * 60)

    current_report = state[
        "report_analysis"
    ]

    historical_records = state[
        "retrieved_documents"
    ]

    comparison = compare_reports(
        current_report=current_report,
        historical_records=historical_records
    )

    print("\nComparison completed.")

    print(comparison)

    return {
        "comparison_result": comparison
    }

def recommendation_node(
    state: HealthcareState
):

    print("\n" + "=" * 60)
    print("NODE: RECOMMENDATION AGENT")
    print("=" * 60)

    current_report = state[
        "report_analysis"
    ]

    historical_records = state[
        "retrieved_documents"
    ]

    comparison = state[
        "comparison_result"
    ]

    recommendations = generate_recommendations(
        current_report=current_report,
        historical_records=historical_records,
        comparison=comparison
    )

    if recommendations is None:
        raise ValueError(
            "Recommendation agent returned None."
        )

    recommendation_data = (
        recommendations.model_dump()
        if hasattr(
            recommendations,
            "model_dump"
        )
        else recommendations
    )

    print("\nRecommendations generated.")

    print(recommendation_data)

    return {
        "recommendations": recommendation_data
    }

def final_response_node(
    state: HealthcareState
):

    analysis = state["report_analysis"]

    comparison = state["comparison_result"]

    recommendations = state["recommendations"]

    response = f"""
## Health Report Analysis

### Current Report

{analysis}

### Historical Comparison

{comparison}

### Recommendations

{recommendations}

### Important Note

This information is generated from the provided
medical records and is intended for informational
purposes only. It should not replace evaluation
or advice from a qualified healthcare professional.
"""

    return {
        "final_response": response
    }