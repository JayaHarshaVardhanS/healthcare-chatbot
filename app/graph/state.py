from typing import Any, Dict, List, TypedDict


class HealthcareState(TypedDict, total=False):

    # Input
    patient_id: str
    uploaded_report: str
    uploaded_report_path: str

    # Report analysis
    report_analysis: Dict[str, Any]

    # RAG
    retrieved_documents: List[Dict[str, Any]]

    # Comparison
    comparison_result: Dict[str, Any]


    # Recommendations
    recommendations: Dict[str, Any]

    # Final answer
    final_response: str