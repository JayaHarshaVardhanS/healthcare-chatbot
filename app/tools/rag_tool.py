from datetime import datetime

from langchain_core.tools import tool

from app.rag.retriever import retrieve_documents


def _parse_date(value: str):
    return datetime.strptime(
        value,
        "%Y-%m-%d",
    ).date()


def retrieve_patient_history(
    patient_id: str,
    query: str,
    current_report_date: str,
    k: int = 5,
):
    """
    Retrieve records belonging to a patient that
    occurred before the current uploaded report.
    """

    if not current_report_date:
        raise ValueError(
            "current_report_date is required "
            "for historical retrieval."
        )

    current_date = _parse_date(
        current_report_date
    )

    # Retrieve more candidates than ultimately needed,
    # because some records may be filtered out.
    candidate_count = max(k * 3, 15)

    documents = retrieve_documents(
        patient_id=patient_id,
        query=query,
        k=candidate_count,
    )

    historical_documents = []

    for document in documents:

        metadata = document.metadata

        record_date = metadata.get(
            "record_date"
        )

        # Ignore demographics or records without dates
        if not record_date:
            continue

        try:
            parsed_record_date = _parse_date(
                record_date
            )
        except ValueError:
            print(
                "Skipping invalid record date:",
                record_date,
            )
            continue

        # Historical means STRICTLY before current report
        if parsed_record_date >= current_date:
            continue

        historical_documents.append(
            {
                "content": document.page_content,
                "metadata": metadata,
            }
        )

    # Put records in chronological order.
    historical_documents.sort(
        key=lambda item: (
            item["metadata"]["record_date"]
        )
    )

    # Keep the most recent k historical records.
    historical_documents = (
        historical_documents[-k:]
    )

    return historical_documents


@tool
def patient_history_rag(
    patient_id: str,
    query: str,
    current_report_date: str,
):
    """
    Retrieve historical medical records belonging
    to a specific patient and dated before the
    current report.
    """

    return retrieve_patient_history(
        patient_id=patient_id,
        query=query,
        current_report_date=current_report_date,
        k=5,
    )