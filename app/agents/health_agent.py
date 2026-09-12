from app.tools.rag_tool import (
    retrieve_patient_history,
)


def run_health_agent(
    patient_id: str,
    report_analysis: dict,
):

    print("\nPatient ID:")
    print(patient_id)

    print("\nReport Analysis:")
    print(report_analysis)

    report_date = report_analysis.get(
        "report_date"
    )

    if not report_date:
        raise ValueError(
            "Report Analyzer did not return "
            "'report_date'. Historical retrieval "
            "cannot continue."
        )

    lab_values = report_analysis.get(
        "lab_values",
        [],
    )

    lab_names = []

    for lab in lab_values:
        name = lab.get("name")

        if name:
            lab_names.append(name)

    if lab_names:
        query = (
            "Historical medical records containing "
            "these laboratory measurements: "
            + ", ".join(lab_names)
        )
    else:
        query = (
            "Historical medical records relevant "
            "to the current patient health report."
        )

    print("\nRAG Query:")
    print(query)

    documents = retrieve_patient_history(
        patient_id=patient_id,
        query=query,
        current_report_date=report_date,
        k=5,
    )

    print(
        f"\nRetrieved {len(documents)} "
        "historical documents."
    )

    for i, document in enumerate(
        documents,
        start=1,
    ):

        print(
            f"\n--- Historical Document {i} ---"
        )

        print(
            "Metadata:",
            document["metadata"],
        )

        print(
            "Content:",
            document["content"][:300],
        )

    return documents