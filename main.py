from pathlib import Path

from app.graph.graph import healthcare_graph
from app.tools.report_parser import parse_pdf


def main():

    patient_id = "P001"

    report_path = (
        "data/patient_records/"
        "P001/2026-03-12_lab_report.pdf"
    )

    print("=" * 60)
    print("HEALTHCARE CHATBOT")
    print("=" * 60)

    print("\nLoading report...")

    report_text = parse_pdf(
        report_path
    )

    print(
        "\nRunning LangGraph workflow..."
    )

    result = healthcare_graph.invoke(
        {
            "patient_id": patient_id,
            "uploaded_report": report_text,
            "uploaded_report_path": report_path
        }
    )

    print("\n")
    print("=" * 60)
    print("FINAL RESPONSE")
    print("=" * 60)

    print(
        result["final_response"]
    )


if __name__ == "__main__":
    main()